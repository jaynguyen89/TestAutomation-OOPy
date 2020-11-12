import unittest

from src.root import Root
from src.utility import browser, faker, check_existence, clear_inputs
from src.helper import assert_checking
from selenium.webdriver.common.keys import Keys
from faker.providers import person
from termcolor import colored

faker.add_provider(person)


class LoginForm:
    def __init__(self):
        self.username_input = browser.find_element_by_css_selector("button[type='submit']")
        self.password_input = browser.find_element_by_id('username')
        self.login_button = browser.find_element_by_id('password')


class LoginFormUITest(unittest.TestCase):
    def test_1_fields_availability(self):
        print(colored('Running: test_1_fields_availability - estimate: 2s', 'yellow'))

        username_input_existed = check_existence('username')
        password_input_existed = check_existence('password')
        login_button_existed = check_existence('login_btn')

        print(colored('\ttest_1_fields_availability: check existence - asserting...', 'blue'))
        self.assertEqual(username_input_existed, True)
        self.assertEqual(password_input_existed, True)
        self.assertEqual(login_button_existed, True)

        print(colored('\ttest_1_fields_availability: passed.', 'cyan'))

    def test_2_missing_inputs(self, form):
        print(colored('Running: test_2_empty_fields - estimate: 3m 30s', 'yellow'))

        clear_inputs(['username', 'password'], 'id')
        form.login_button.send_keys(Keys.ENTER)

        print(colored('\ttest_2_empty_fields: all fields empty - asserting...', 'blue'))
        try:
            assert_checking(self, 'Username and Password are required.')
        except AssertionError:
            assert_checking(self, 'No record in Juice matches the data.')

        form.username_input.send_keys('testing')
        form.login_button.send_keys(Keys.ENTER)

        print(colored('\ttest_2_empty_fields: password empty - asserting...', 'blue'))
        try:
            assert_checking(self, 'Username and Password are required.')
        except AssertionError:
            assert_checking(self, 'No record in Juice matches the data.')

        clear_inputs(['username', 'password'], 'id')
        form.password_input.send_keys('testing')
        form.login_button.send_keys(Keys.ENTER)

        print(colored('\ttest_2_empty_fields: username empty - asserting...', 'blue'))
        try:
            assert_checking(self, 'Username and Password are required.')
        except AssertionError:
            assert_checking(self, 'No record in Juice matches the data.')

        print(colored('\ttest_2_empty_fields: passed.', 'cyan'))

    def test_3_incorrect_credentials(self, form):
        print(colored('Running: test_3_incorrect_credentials - estimate: 2m 10s', 'yellow'))

        print(colored('\ttest_3_incorrect_credentials: both fields incorrect - asserting...', 'blue'))
        clear_inputs(['username', 'password'], 'id')
        Root.login_user(browser, {'username': faker.last_name(), 'password': faker.word()})
        try:
            assert_checking(self, 'No user in Juice matches the login credentials.')
        except AssertionError:
            assert_checking(self, 'No record in Juice matches the data.')

        print(colored('\ttest_3_incorrect_credentials: password incorrect - asserting...', 'blue'))
        clear_inputs(['username', 'password'], 'id')
        Root.login_user(browser, {'username': 'JayNG', 'password': faker.word()})
        try:
            assert_checking(self, 'No user in Juice matches the login credentials.')
        except AssertionError:
            assert_checking(self, 'No record in Juice matches the data.')

        print(colored('\ttest_3_incorrect_credentials: passed.', 'cyan'))
