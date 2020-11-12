import unittest
from time import sleep
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, click_action_button, get_table_headers
from src.helper import get_random_row_in_account_table


class AccountRevivalTest(unittest.TestCase):
    def test_1_unconfirmed(self):
        print(colored('Running: test_1_unconfirmed - estimate: 3s', 'yellow'))
        account_table_headers = get_table_headers()

        inactive_user_row = get_random_row_in_account_table(active=False)
        inactive_user_cols = inactive_user_row.find_elements_by_tag_name('td')
        click_action_button(inactive_user_cols)
        sleep(SLEEP_INTERVAL)

        confirmation = browser.switch_to_alert()
        print(colored('\ttest_1_unconfirmed: cancel revival - asserting...', 'blue'))
        self.assertEqual(confirmation.text, 'Revive the account ' + inactive_user_cols[
            account_table_headers.index('Full Name')] + '. Continue?')

        active_users_table = browser.find_element_by_xpath('//tbody[@class="MuiTableBody-root"]')
        active_users_rows = active_users_table.find_elements_by_tag_name('tr')
        active_users = [row for row in active_users_rows if len(row.find_elements_by_tag_name('td')) > 0]

        user_names = []
        for user in active_users:
            user_names.append(
                user.find_elements_by_tag_name('td')[account_table_headers.index('Full Name')].get_attribute(
                    'innerHTML'))

        print(colored('\ttest_1_unconfirmed: active users - asserting...', 'blue'))
        assert inactive_user_cols[account_table_headers.index('Full Name')] not in user_names

        if len(browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')) > 1:
            inactive_users_table = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')[1]
            inactive_users_rows = inactive_users_table.find_elements_by_tag_name('tr')
            inactive_users = [row for row in inactive_users_rows if len(row.find_elements_by_tag_name('td')) > 0]

            in_user_names = []
            for user in inactive_users:
                in_user_names.append(
                    user.find_elements_by_tag_name('td')[account_table_headers.index('Full Name')].get_attribute(
                        'innerHTML'))

            print(colored('\ttest_1_unconfirmed: inactive users - asserting...', 'blue'))
            assert inactive_user_cols[account_table_headers.index('Full Name')] in in_user_names

        print(colored('\ttest_1_unconfirmed: passed.', 'cyan'))

    @staticmethod
    def test_2_confirm_no_network():
        print(colored('Running: test_2_confirm_no_network - estimate: 40s', 'yellow'))
        prompt_to_disable_network()

        inactive_user_row = get_random_row_in_account_table(active=False)
        inactive_user_cols = inactive_user_row.find_elements_by_tag_name('td')
        click_action_button(inactive_user_cols)
        sleep(SLEEP_INTERVAL)

        browser.switch_to_alert().accept()
        sleep(9+SLEEP_INTERVAL)

        print(colored('\ttest_2_confirm_no_network: revival failed - asserting...', 'blue'))
        confirmation = browser.switch_to_alert()
        assert 'Error occurred while reviving account' in confirmation.text

        confirmation.accept()

        print(colored('\ttest_2_confirm_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/ManageUser')

    @staticmethod
    def test_3_confirm_success():
        print(colored('Running: test_3_confirm_success - estimate: 40s', 'yellow'))
        account_table_headers = get_table_headers()

        inactive_user_row = get_random_row_in_account_table(active=False)
        inactive_user_cols = inactive_user_row.find_elements_by_tag_name('td')
        click_action_button(inactive_user_cols)
        sleep(SLEEP_INTERVAL)

        browser.switch_to_alert().accept()
        sleep(2*SLEEP_INTERVAL)

        active_users_table = browser.find_element_by_xpath('//tbody[@class="MuiTableBody-root"]')
        active_users_rows = active_users_table.find_elements_by_tag_name('tr')
        active_users = [row for row in active_users_rows if len(row.find_elements_by_tag_name('td')) > 0]

        user_names = []
        for user in active_users:
            user_names.append(
                user.find_elements_by_tag_name('td')[account_table_headers.index('Full Name')].get_attribute(
                    'innerHTML'))

        print(colored('\ttest_3_confirm_success: active users - asserting...', 'blue'))
        assert inactive_user_cols[account_table_headers.index('Full Name')] in user_names

        if len(browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')) > 1:
            inactive_users_table = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')[1]
            inactive_users_rows = inactive_users_table.find_elements_by_tag_name('tr')
            inactive_users = [row for row in inactive_users_rows if len(row.find_elements_by_tag_name('td')) > 0]

            in_user_names = []
            for user in inactive_users:
                in_user_names.append(
                    user.find_elements_by_tag_name('td')[account_table_headers.index('Full Name')].get_attribute(
                        'innerHTML'))

            print(colored('\ttest_3_confirm_success: inactive users - asserting...', 'blue'))
            assert inactive_user_cols[account_table_headers.index('Full Name')] not in in_user_names

        print(colored('\ttest_1_unconfirmed: passed.', 'cyan'))


if __name__ == '__main__':
    runAccountRevivalTest = AccountRevivalTest()
    print(colored('AccountRevivalTest - ' + str(runAccountRevivalTest.countTestCases()) +
                  ' tests in account form.', 'green'))
    runAccountRevivalTest.test_1_unconfirmed()
    runAccountRevivalTest.test_2_confirm_no_network()
    runAccountRevivalTest.test_3_confirm_success()
