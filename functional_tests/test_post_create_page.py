from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from seleniumlogin import force_login
from posts.models import Subreddit

class TestPostCreatePage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()  
        self.subreddit = Subreddit.objects.create(subreddit_name='test', created_by=self.user)
        self.post_create_page = reverse('post_create', args=[self.subreddit.url])

    def tearDown(self):
        self.browser.close()    

    def test_post_create_requires_login(self):
        self.browser.get(self.live_server_url + self.post_create_page)
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/login/?next=%s' % self.post_create_page
            )

    def test_post_create_form_is_displayed_when_logged_in(self):
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + self.post_create_page)
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME, 'post-create-form'))
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + self.post_create_page
            )

    def test_post_create_form_invalid(self):
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + self.post_create_page)
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + self.post_create_page)

    def test_post_create_form_success(self):
        force_login(self.user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + self.post_create_page)
        self.browser.find_element('name', 'subreddit').click()
        self.browser.find_element(By.XPATH, '//*[@id="id_subreddit"]/option[2]').click()
        self.browser.find_element('name', 'post_title').send_keys('test post')
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + reverse('post_detail', args=[self.subreddit.url, self.subreddit.posts.get(id=1).url]))
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'h2').text, 
            'test post'
            )