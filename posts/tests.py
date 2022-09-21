from django.test import TestCase
from .models import Subreddit, Post
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta

class SubredditModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
       
    def test_sorted_new_returns_empty_queryset_when_0_posts(self):
        self.assertEqual(len(self.subreddit.sorted_new()), 0)

    def test_sorted_new_returns_post_when_1_post(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        actual_post = list(self.subreddit.sorted_new())
        expected_post = [self.post]
        self.assertEqual(expected_post, actual_post)

    def test_sorted_new_returns_sorted_posts(self):
        self.post_tomorrow = self.subreddit.posts.create(created_by=self.user)
        self.post_today = self.subreddit.posts.create(created_by=self.user)
        self.post_yesterday = self.subreddit.posts.create(created_by=self.user)
        
        self.post_tomorrow.created_at = datetime.now() + timedelta(1)
        self.post_tomorrow.save()
        self.post_today.created_at = datetime.now()
        self.post_today.save()
        self.post_yesterday.created_at = datetime.now() - timedelta(1)
        self.post_yesterday.save()

        self.assertEqual(
            list(self.subreddit.sorted_new()),
            [self.post_tomorrow, self.post_today, self.post_yesterday]
            )
    
    def test_sorted_top_returns_empty_queryset_when_0_posts(self):
        self.assertEqual(len(self.subreddit.sorted_top()), 0)

    def test_sorted_top_returns_post_when_1_post(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        actual_post = list(self.subreddit.sorted_top())
        expected_post = [self.post]
        self.assertEqual(expected_post, actual_post)

    def test_sorted_top_returns_sorted_posts(self):
        self.post_low = self.subreddit.posts.create(created_by=self.user, score = -1)
        self.post_middle = self.subreddit.posts.create(created_by=self.user, score = 0)
        self.post_high = self.subreddit.posts.create(created_by=self.user, score = 1)

        self.assertEqual(
            list(self.subreddit.sorted_top()), 
            [self.post_high, self.post_middle, self.post_low]
            )
    
class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
           
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

    def test_preview_returns_empty_string_when_post_body_is_none(self):
        self.post = self.subreddit.posts.create(created_by=self.user)
        self.assertEqual(self.post.preview(), '')

    def test_preview_returns_post_body_when_200_characters_or_fewer(self):
        self.post = self.subreddit.posts.create(created_by=self.user, post_body = 10 * 'a')
        self.assertEqual(self.post.post_body, self.post.preview())

    def test_preview_returns_preview_when_above_200_characters(self):
        self.post = self.subreddit.posts.create(created_by=self.user, post_body = 300 * 'a')
        self.assertEqual(200, len(self.post.preview()))
        self.assertEqual('...', self.post.preview()[-3:])

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
        self.assertRedirects(response, reverse('post_detail', args=[self.subreddit.url, 'test_post']))
        self.assertEqual(str(Post.objects.get(post_title='test_post')), 'test_post')

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
        response = self.client.get(reverse('post_detail', args=[self.subreddit.url, 'test_post']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_detail_view_comment_requires_login(self):
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, 'test_post']), {'comment_text': 'test'})
        self.assertRedirects(response, '/login/?next=/r/test/comments/test_post/')

    def test_post_detail_view_comment_form_empty(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, 'test_post']), {'comment_text': ''})
        self.assertFormError(response, 'form', 'comment_text', 'This field is required.')

    def test_post_detail_view_comment_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, 'test_post']), {'comment_text': 'test'})
        self.assertRedirects(response, reverse('post_detail', args=[self.subreddit.url, 'test_post']))
        self.assertEqual(len(self.post.comments.all()), 1)

    def test_post_detail_view_comment_reply_requires_login(self):
        self.comment = self.post.comments.create(comment_text='test_comment', created_by=self.user)
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, 'test_post']), {'comment_text': 'test', 'reply': self.comment})
        self.assertRedirects(response, '/login/?next=/r/test/comments/test_post/')

    def test_post_detail_view_comment_reply_form_empty(self):
        self.comment = self.post.comments.create(comment_text='test_comment', created_by=self.user)
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, 'test_post']), {'comment_text': '', 'reply': self.comment})
        self.assertFormError(response, 'form', 'comment_text', 'This field is required.')

    def test_post_detail_view_comment_reply_success(self):
        self.comment = self.post.comments.create(comment_text='test_comment', created_by=self.user)
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.subreddit.url, 'test_post']), {'comment_text': 'test', 'reply_id': self.comment.id})
        self.assertRedirects(response, reverse('post_detail', args=[self.subreddit.url, 'test_post']))
        self.assertEqual(len(self.post.comments.all()), 2)
        self.assertEqual(len(self.comment.replies.all()), 1)