from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from seleniumlogin import force_login
from posts.models import Subreddit

class TestPostVotingAnonymous(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
        self.post = self.subreddit.posts.create(post_title='test post', created_by=self.user)
        self.browser.get(self.live_server_url + reverse('post_detail', args=[self.subreddit.url, self.post.url]))

    def tearDown(self):
        self.browser.close()    

    def test_post_vote_increases(self):
        self.browser.find_element(By.CLASS_NAME, 'upvote').click()
        self.assertEqual('1', self.browser.find_element(By.CLASS_NAME, 'post-score').text)
        
    def test_post_vote_decreases(self):
        self.browser.find_element(By.CLASS_NAME, 'downvote').click()
        self.assertEqual('-1', self.browser.find_element(By.CLASS_NAME, 'post-score').text)

    def test_post_vote_only_upvote_once(self):
        for x in range(2):
            self.browser.find_element(By.CLASS_NAME, 'upvote').click()
        self.assertEqual('1', self.browser.find_element(By.CLASS_NAME, 'post-score').text)

    def test_post_vote_only_downvote_once(self):
        for x in range(2):
            self.browser.find_element(By.CLASS_NAME, 'downvote').click()
        self.assertEqual('-1', self.browser.find_element(By.CLASS_NAME, 'post-score').text)

class TestPostVotingLoggedIn(TestPostVotingAnonymous):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
        self.post = self.subreddit.posts.create(post_title='test post', created_by=self.user)
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + reverse('post_detail', args=[self.subreddit.url, self.post.url]))