from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class TestLoginPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()  

    def tearDown(self):
        self.browser.close()

    def test_login_form_is_displayed(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME, 'login-form'))
    
    def test_login_form_invalid(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

    def test_login_form_success(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element('name', 'username').send_keys('testuser')
        self.browser.find_element('name', 'password').send_keys('password')
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(self.browser.find_element(By.CLASS_NAME, 'current-user').text, 'u/testuser')
        