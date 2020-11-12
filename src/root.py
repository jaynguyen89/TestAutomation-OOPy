from time import sleep
from termcolor import colored
from src.utility import TEST_URL, SLEEP_INTERVAL, LOGIN_CREDENTIALS, logout, trigger_navbar, clear_inputs
from selenium.common.exceptions import NoSuchElementException


# This script handle the most common steps in testing that will be required by most of other tests
# It launches the website in Chrome and opens Login page


class Root:
    @staticmethod
    def open_juice_app_on_chrome(browser):
        browser.maximize_window()
        browser.get(TEST_URL)

    @staticmethod
    def login_user(browser, credentials):
        login_btn = browser.find_element_by_css_selector("button[type='submit']")

        username_input = browser.find_element_by_id('username')
        password_input = browser.find_element_by_id('password')

        clear_inputs(['username', 'password'], 'id')

        username_input.send_keys(credentials['username'])
        password_input.send_keys(credentials['password'])

        login_btn.click()

    @staticmethod
    def navigate_to(browser, section):
        main_section_id = section.split('/')[0]
        sub_section_id = "/" + section.split('/')[1]

        trigger_navbar()

        browser.find_element_by_id(main_section_id).click()
        sleep(SLEEP_INTERVAL)
        browser.find_element_by_id(sub_section_id).click()

        trigger_navbar()

    @staticmethod
    def tear_down_on_test_done(browser):
        try:
            logout()
        except NoSuchElementException:
            browser.quit()

        browser.quit()


def rerun_setup(browser, section):
    logout()
    sleep(2*SLEEP_INTERVAL)
    Root.login_user(browser, {'username': LOGIN_CREDENTIALS['username'], 'password': LOGIN_CREDENTIALS['password']})
    Root.navigate_to(browser, section)


def prompt_to_disable_network():
    print(colored('\tPlease turn off network connection before this test executes. Test waits for ' + str(15*SLEEP_INTERVAL) + 's...', 'red'))
    sleep(15*SLEEP_INTERVAL)
    print('\tTest now continues...')


def prompt_to_enable_network():
    print(colored('\tTest done! Please connect to network again. Test waits for ' + str(15*SLEEP_INTERVAL) + 's...', 'red'))
    sleep(15*SLEEP_INTERVAL)


def prompt_to_enable_network_and_setup(browser, section):
    print(colored('\tTest done! Please connect to network again. Test waits for ' + str(15*SLEEP_INTERVAL) + 's...', 'red'))
    sleep(15*SLEEP_INTERVAL)

    print(colored('\tRe-setup test environment...', 'red'))
    try:
        rerun_setup(browser, section)
    except:
        print(colored('\tNo network connected. Test abort!', 'red'))
        browser.quit()


class LocalStorage:
    def __init__(self, browser):
        self.browser = browser

    def __len__(self):
        return self.browser.execute_script("return window.localStorage.length;")

    def items(self):
        return self.browser.execute_script(
            "var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items; ")

    def keys(self):
        return self.browser.execute_script(
            "var ls = window.localStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys; ")

    def get(self, key):
        return self.browser.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.browser.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.browser.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.browser.execute_script("window.localStorage.clear();")

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
