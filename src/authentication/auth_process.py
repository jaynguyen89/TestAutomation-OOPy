import unittest
from time import sleep
from src.root import Root, LocalStorage
from src.utility import SLEEP_INTERVAL, browser, faker, logout, clear_inputs
from faker.providers import person
from termcolor import colored
from src.authentication.login_form_ui import LoginFormUITest

faker.add_provider(person)


class LoginForm:
    def __init__(self):
        self.username_input = browser.find_element_by_css_selector("button[type='submit']")
        self.password_input = browser.find_element_by_id('username')
        self.login_button = browser.find_element_by_id('password')


class AuthProcessTest(unittest.TestCase):
    @staticmethod
    def test_1_correct_credentials():
        print(colored('Running: test_1_correct_credentials - estimate: 2s', 'yellow'))

        clear_inputs(['username', 'password'], 'id')
        Root.login_user(browser, {'username': 'JayNG', 'password': 'password'})

        print(colored('\ttest_1_correct_credentials: login successful - asserting...', 'blue'))
        assert "No user in Juice matches the login credentials." not in browser.page_source
        assert "Username and Password are required." not in browser.page_source

        # check for user menu

        print(colored('\ttest_1_correct_credentials: passed.', 'cyan'))

    def test_2_session_data(self):
        print(colored('Running: test_2_session_data - estimate: 3s', 'yellow'))

        local_storage = LocalStorage(browser)
        sleep(2*SLEEP_INTERVAL)
        session_data = local_storage.get('currentUser')

        print(colored('\ttest_2_session_data: local storage - asserting...', 'blue'))
        self.assertIsNotNone(session_data)

        # also check detailed data

        print(colored('\ttest_2_session_data: passed.', 'cyan'))

    def test_3_logout(self):
        print(colored('Running: test_3_logout - estimate: 20s', 'yellow'))

        logout()

        print(colored('\ttest_3_logout: on login page - asserting...', 'blue'))
        sleep(5*SLEEP_INTERVAL)
        login_form_test = LoginFormUITest()
        login_form_test.test_1_fields_availability()

        print(colored('\ttest_3_logout: local storage - asserting...', 'blue'))
        local_storage = LocalStorage(browser)

        sleep(2*SLEEP_INTERVAL)
        self.assertIsNone(local_storage.get('currentUser'))

        print(colored('\ttest_3_logout: passed.', 'cyan'))
