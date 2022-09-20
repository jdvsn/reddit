from django.test import TestCase
from .models import Subreddit, Post
from django.contrib.auth.models import User
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
        
    def comment_count_returns_0_when_no_comments(self):
        self.post = self.subreddit.posts.create(subreddit=self.subreddit, created_by=self.user)
        self.assertEqual(len(self.post.comments.all()), self.post.comment_count())

    def comment_count_returns_correct_count(self):
        self.post = self.subreddit.posts.create(subreddit=self.subreddit, created_by=self.user)
        pass

    def preview_uses_post_body_when_200_characters_or_fewer(self):
        

