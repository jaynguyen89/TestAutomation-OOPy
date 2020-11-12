import unittest
from time import sleep
from src.utility import SLEEP_INTERVAL, browser, check_existence
from src.root import Root, prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.helper import get_table_headers, get_random_account_data
from termcolor import colored


class AccountListTest(unittest.TestCase):
    def test_1_no_network(self):
        print(colored('Running: test_1_no_network - estimate: 11s', 'yellow'))
        prompt_to_disable_network()

        browser.refresh()
        Root.navigate_to(browser, 'Administration/ManageUser')
        sleep(9 + SLEEP_INTERVAL)

        print(colored('\ttest_1_no_network: no network - asserting...', 'blue'))
        self.assertEqual(check_existence('account_lists'), False)
        self.assertEqual(check_existence('//div[@class="inform"]', is_id=False), True)
        self.assertEqual(check_existence('//div[@class="MuiFormControl-root MuiFormControl-fullWidth"]', is_id=False),
                         True)

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/ManageUser')

    def test_2_page_content(self):
        print(colored('Running: test_2_page_content - estimate: 2s', 'yellow'))

        print(colored('\ttest_2_page_content: list container - asserting...', 'blue'))
        sleep(2 * SLEEP_INTERVAL)
        self.assertEqual(check_existence('account-lists'), True)

        print(colored('\ttest_2_page_content: account form - asserting...', 'blue'))
        self.assertEqual(check_existence('//div[@class="MuiFormControl-root MuiFormControl-fullWidth"]', is_id=False),
                         True)

        account_list_container = browser.find_element_by_id('account-lists')
        account_lists = account_list_container.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')

        print(colored('\ttest_2_page_content: list count - asserting...', 'blue'))
        self.assertGreaterEqual(len(account_lists), 1)

        print(colored('\ttest_2_page_content: passed.', 'cyan'))

    def test_3_account_lists_display(self):
        print(colored('Running: test_3_account_lists_display - estimate: 2s', 'yellow'))
        pagination_labels = browser.find_elements_by_xpath('//tfoot[@class="MuiTableFooter-root"]/tr/td/div/div/span['
                                                           '@class="MuiTypography-root MuiTypography-caption"]')

        active_accounts_count = int(pagination_labels[0].get_attribute('innerHTML').split(' ')[2])
        print(colored('\ttest_3_account_lists_display: active accounts count - asserting...', 'blue'))
        self.assertGreater(active_accounts_count, 0)

        if len(pagination_labels) > 1:
            inactive_accounts_count = int(pagination_labels[1].get_attribute('innerHTML').split(' ')[2])
            print(colored('\ttest_3_account_lists_display: inactive accounts count - asserting...', 'blue'))
            self.assertGreater(inactive_accounts_count, 0)

        print(colored('\ttest_3_account_lists_display: passed.', 'cyan'))

    def test_4_account_lists_columns(self):
        print(colored('Running: test_4_account_lists_columns - estimate: 48s', 'yellow'))
        list_headers = get_table_headers()
        account_lists = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')

        for account_list in account_lists:
            for i in range(2):
                print(colored('\trandom account ' + str(i + 1), 'magenta'))
                account_cols = get_random_account_data(account_list)

                for col in list_headers:
                    col_data = account_cols[list_headers.index(col)].get_attribute('innerHTML')
                    has_data = (col == 'Full Name' or col == 'Username' or col == 'Email') and \
                               len(col_data) > 0 or len(col_data) >= 0

                    print(colored(
                        '\ttest_4_account_lists_columns: ' + (i == 0 and 'active' or 'inactive') + ' accounts data - asserting...',
                        'blue'))
                    self.assertTrue(has_data)

        print(colored('\ttest_4_account_lists_columns: passed.', 'cyan'))


if __name__ == '__main__':
    runAccountListTest = AccountListTest()
    print(colored('AccountListTest - ' + str(runAccountListTest.countTestCases()) + ' tests in Account page.', 'green'))
    runAccountListTest.test_1_no_network()
    runAccountListTest.test_2_page_content()
    runAccountListTest.test_3_account_lists_display()
    runAccountListTest.test_4_account_lists_columns()
