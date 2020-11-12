import unittest
from time import sleep
from datetime import date, datetime
from termcolor import colored
from selenium.webdriver.common.keys import Keys
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, clear_inputs, get_random_table_data,\
    pick_random_dropdown_item, click_fab_button, click_save_button


class AccountCreateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 11s', 'yellow'))
        prompt_to_disable_network()

        browser.find_element_by_id('save-button').send_keys(Keys.ENTER)
        sleep(9+SLEEP_INTERVAL)

        confirmation = browser.switch_to_alert()
        print(colored('\ttest_1_no_network: create failed - asserting...', 'blue'))
        assert 'Error occurred while creating new account' in confirmation.text

        confirmation.accept()

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/ManageUser')

    def test_2_missing_required_inputs(self):
        # full name, username, email, org
        print(colored('Running: test_2_missing_required_inputs - estimate: 11s', 'yellow'))

        pass

    def test_3_redundant_account(self):
        pass

    def test_4_create_success(self):
        pass


if __name__ == '__main__':
    runAccountCreateTest = AccountCreateTest()
    print(colored('AccountCreateTest - ' + str(runAccountCreateTest.countTestCases()) + ' tests in account form.', 'green'))
    runAccountCreateTest.test_1_no_network()
    runAccountCreateTest.test_2_missing_required_inputs()
    runAccountCreateTest.test_3_redundant_account()
    runAccountCreateTest.test_4_create_success()
