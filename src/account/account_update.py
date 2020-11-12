import unittest
from time import sleep
from datetime import date
from termcolor import colored
from selenium.webdriver.common.keys import Keys
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, get_random_table_row, close_modal, get_table_headers,\
    pick_random_dropdown_item, clear_inputs, click_update_button, click_action_button
from src.helper import get_random_row_in_account_table


class AccountUpdateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 3s', 'yellow'))
        active_user_row = get_random_row_in_account_table()
        active_user_cols = active_user_row.find_elements_by_tag_name('td')
        click_action_button(active_user_cols)
        sleep(2*SLEEP_INTERVAL)

        browser.find_element_by_id('account-password').send_keys('testing')
        browser.find_element_by_id('confirm-password').send_keys('testing')

        prompt_to_disable_network()

        browser.find_element_by_id('save-button').send_keys(Keys.ENTER)
        sleep(9+SLEEP_INTERVAL)

        confirmation = browser.switch_to_alert()
        print(colored('\ttest_1_no_network: create failed - asserting...', 'blue'))
        assert 'Error occurred while updating account' in confirmation.text

        confirmation.accept()

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/ManageUser')

    def test_2_missing_required_fields(self):
        # full name, username, email, org
        pass

    def test_3_input_validations(self):
        pass

    def test_4_update_success(self):
        pass


if __name__ == '__main__':
    runAccountUpdateTest = AccountUpdateTest()
    print(colored('AccountUpdateTest - ' + str(runAccountUpdateTest.countTestCases()) + ' tests in account form.','green'))
    runAccountUpdateTest.test_1_no_network()
    runAccountUpdateTest.test_2_missing_required_fields()
    runAccountUpdateTest.test_3_input_validations()
    runAccountUpdateTest.test_4_update_success()
