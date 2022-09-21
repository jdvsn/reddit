from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from seleniumlogin import force_login

class TestSubredditCreatePage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()  

    def tearDown(self):
        self.browser.close()

    def test_subreddit_create_requires_login(self):
        self.browser.get(self.live_server_url + reverse('subreddit_create'))
        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/?next=/subreddits/create/')

    def test_subreddit_create_form_is_displayed(self):
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + reverse('subreddit_create'))
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME, 'subreddit-create-form'))
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('subreddit_create'))

    def test_subreddit_create_form_invalid(self):
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + reverse('subreddit_create'))
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('subreddit_create'))


    def test_subreddit_create_form_success(self):
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + reverse('subreddit_create'))
        self.browser.find_element('name', 'subreddit_name').send_keys('test')
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('subreddit', args=['test']))
        self.assertEqual(self.browser.find_element(By.TAG_NAME, 'h1').text, 'r/test')