from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By

class TestRegisterPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_user_creation_form_is_displayed(self):
        self.browser.get(self.live_server_url + reverse('register'))
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME, 'register-form'))
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + reverse('register')
            )
    
    def test_user_creation_form_invalid(self):
        self.browser.get(self.live_server_url + reverse('register'))
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + reverse('register')
            )

    def test_user_creation_form_success(self):
        self.browser.get(self.live_server_url + reverse('register'))
        self.browser.find_element('name', 'username').send_keys('testuser')
        self.browser.find_element('name', 'password1').send_keys('testpassword')
        self.browser.find_element('name', 'password2').send_keys('testpassword')
        self.browser.find_element('name', 'email').send_keys('user@test.com')
        self.browser.find_element('name', 'submit').click()
        self.assertEqual(
            self.browser.find_element(By.CLASS_NAME, 'current-user').text, 
            'u/testuser'
            )