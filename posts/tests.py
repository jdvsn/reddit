from django.test import TestCase
from .models import Subreddit, Post
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from datetime import datetime, timedelta
       
class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.subreddit_creator = User.objects.create(username='subreddit creator')
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.subreddit_creator)
           
    def test_comment_count_returns_0_when_no_comments(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.assertEqual(len(self.post.comments.all()), self.post.comment_count())

    def test_comment_count_returns_correct_count(self):
        self.post_5 = self.subreddit.posts.create(created_by=self.user)
        self.post_100 = self.subreddit.posts.create(created_by=self.user)
        for x in range(5):
            self.post_5.comments.create(created_by=self.user)
        for x in range(100):
            self.post_100.comments.create(created_by=self.user)
        self.assertEqual(5, self.post_5.comment_count())
        self.assertEqual(100, self.post_100.comment_count())

    def test_preview_returns_none_when_post_body_is_empty(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.assertEqual(self.post.preview(), None)

    def test_preview_returns_post_body_when_200_characters_or_fewer(self):
        self.post = self.subreddit.posts.create(created_by=self.user, post_body = 10 * 'a')
        self.assertEqual(self.post.post_body, self.post.preview())

    def test_preview_returns_preview_when_above_200_characters(self):
        self.post = self.subreddit.posts.create(created_by=self.user, post_body = 300 * 'a')
        self.assertEqual(200, len(self.post.preview()))
        self.assertEqual('...', self.post.preview()[-3:])

    def test_can_delete_returns_true_when_post_creator(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.assertTrue(self.post.can_delete(self.user)) # returns True when post creator
        self.assertFalse(self.user in self.subreddit.moderators.all()) # and not a subreddit moderator
        self.assertFalse(self.user.has_perm('posts.admin_delete_post')) # and not an admin

    def test_can_delete_returns_true_when_subreddit_moderator(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.subreddit_moderator = User.objects.create(username='subreddit moderator')
        self.subreddit.moderators.add(self.subreddit_moderator)
        self.assertTrue(self.post.can_delete(self.subreddit_moderator)) # return True when a subreddit moderator
        self.assertNotEqual(self.post.created_by, self.subreddit_moderator) # and not post creator
        self.assertFalse(self.user.has_perm('posts.admin_delete_post')) # and not an admin

    def test_can_delete_returns_true_when_admin(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.admin = User.objects.create(username='admin')
        self.admin.user_permissions.add(Permission.objects.get(name='admin delete post'))
        self.assertTrue(self.post.can_delete(self.admin)) # return True when admin
        self.assertNotEqual(self.post.created_by, self.admin) # and not post creator
        self.assertFalse(self.user in self.subreddit.moderators.all()) # and not a subreddit moderator
        
    def test_can_delete_returns_false_when_not_post_creator_or_moderator_or_admin(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.user_2 = User.objects.create()
        self.assertFalse(self.post.can_delete(self.user_2))

    def test_can_delete_returns_false_when_moderator_of_a_different_subreddit(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.user_2 = User.objects.create()
        self.subreddit_2 = Subreddit.objects.create(created_by=self.user_2)
        self.subreddit_2.moderators.add(self.user_2)
        self.assertFalse(self.post.can_delete(self.user_2))
        
class SubredditCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    def test_subreddit_create_view_requires_login(self):
        response = self.client.get(reverse('subreddit_create'), follow=True)
        self.assertRedirects(response, '/login/?next=/subreddits/create/')
        response = self.client.post(reverse('subreddit_create'), follow=True)
        self.assertRedirects(response, '/login/?next=/subreddits/create/')

    def test_subreddit_create_view_show_form(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('subreddit_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/subreddit_create.html')

    def test_subreddit_create_view_form_is_blank(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('subreddit_create'), {})  
        self.assertFormError(response, 'form', 'subreddit_name', 'This field is required.')

    def test_subreddit_create_view_subreddit_already_exists(self):
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('subreddit_create'), {'subreddit_name':'test'})
        self.assertFormError(response, 'form', 'subreddit_name', 'A subreddit with this name already exists.')

    def test_subreddit_create_view_subreddit_success(self):
        self.name = 'test'
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('subreddit_create'), {'subreddit_name': self.name})
        self.assertRedirects(response, reverse('subreddit', args=[self.name]))
        self.assertEqual(str(Subreddit.objects.get(subreddit_name=self.name)), self.name)

class PostCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()  
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
        self.post_create_url = reverse('post_create', args=[self.subreddit.url])

    def test_post_create_view_requires_login(self):
        response = self.client.get(self.post_create_url, follow=True)
        self.assertRedirects(response, '/login/?next=/r/%s/submit/' % self.subreddit.url)
        response = self.client.post(self.post_create_url, follow=True)
        self.assertRedirects(response, '/login/?next=/r/%s/submit/' % self.subreddit.url)  

    def test_post_create_view_show_form(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.post_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')  

    def test_post_create_view_subreddit_not_selected(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.post_create_url, {'post_title': 'test_post'})  
        self.assertFormError(response, 'form', 'subreddit', 'This field is required.')

    def test_post_create_view_post_title_is_blank(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.post_create_url, {'subreddit': self.subreddit.id})  
        self.assertFormError(response, 'form', 'post_title', 'This field is required.')

    def test_post_create_view_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.post_create_url, {'subreddit': self.subreddit.id,'post_title': 'test_post'})
        test_post = Post.objects.get(post_title='test_post')  
        self.assertRedirects(response, reverse('post_detail', args=[self.subreddit.url, test_post.url]))

class PostDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()  
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
        self.post = self.subreddit.posts.create(post_title='test_post', created_by=self.user)

    def test_post_detail_view_post_does_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[self.subreddit.url, '404']))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_show_post(self):
        response = self.client.get(reverse('post_detail', args=[self.subreddit.url, self.post.url]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_detail_view_comment_requires_login(self):
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, self.post.url]), {'comment_text': 'test'})
        self.assertRedirects(response, '/login/?next=%s' % (reverse('post_detail', args=[self.subreddit.url, self.post.url])))

    def test_post_detail_view_comment_form_empty(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, self.post.url]), {'comment_text': ''})
        self.assertFormError(response, 'form', 'comment_text', 'This field is required.')

    def test_post_detail_view_comment_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, self.post.url]), {'comment_text': 'test'})
        self.assertRedirects(response, reverse('post_detail', args=[self.subreddit.url, self.post.url]))
        self.assertEqual(len(self.post.comments.all()), 1)

    def test_post_detail_view_comment_reply_requires_login(self):
        self.comment = self.post.comments.create(comment_text='test_comment', created_by=self.user)
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, self.post.url]), {'comment_text': 'test', 'parent_id': self.comment.id})
        self.assertRedirects(response, '/login/?next=%s' % (reverse('post_detail', args=[self.subreddit.url, self.post.url])))

    def test_post_detail_view_comment_reply_form_empty(self):
        self.comment = self.post.comments.create(comment_text='test_comment', created_by=self.user)
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, self.post.url]), {'comment_text': '', 'parent_id': self.comment.id})
        self.assertFormError(response, 'form', 'comment_text', 'This field is required.')

    def test_post_detail_view_comment_reply_success(self):
        self.comment = self.post.comments.create(comment_text='test_comment', created_by=self.user)
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, self.post.url]), {'comment_text': 'test', 'parent_id': self.comment.id})
        self.assertRedirects(response, reverse('post_detail', args=[self.subreddit.url, self.post.url]))
        self.assertEqual(len(self.post.comments.all()), 2)
        self.assertEqual(len(self.comment.replies.all()), 1)