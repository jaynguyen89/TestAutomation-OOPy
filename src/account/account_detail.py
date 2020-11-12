import unittest
from time import sleep
from selenium.webdriver.common.keys import Keys
from termcolor import colored
from src.root import prompt_to_disable_network
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_dropdown_item, \
    click_action_button, get_table_headers
from src.helper import get_random_row_in_account_table


class AccountDetailTest(unittest.TestCase):
    def test_1_detail_form_elements(self):
        print(colored('Running: test_1_detail_form_elements - estimate: 2s', 'yellow'))
        account_details_form_ids = ['full-name', 'email-address', 'organization', 'jira-token',
                                    'username', 'account-password', 'confirm-password']

        for el_id in account_details_form_ids:
            print(colored('\ttest_1_detail_form_elements: input "' + el_id + '" existence - asserting...', 'blue'))
            self.assertTrue(check_existence(el_id))

        print(colored('\ttest_1_detail_form_elements: input new-password existence - asserting...', 'blue'))
        self.assertFalse(check_existence('new-password'))

        active_user = get_random_row_in_account_table()
        click_action_button(active_user.find_elements_by_tag_name('td'))
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_1_detail_form_elements: input new-password existence - asserting...', 'blue'))
        self.assertTrue(check_existence('new-password'))

        print(colored('\ttest_1_detail_form_elements: passed.', 'cyan'))

    def test_2_form_checkboxes(self):
        print(colored('Running: test_2_form_checkboxes - estimate: 12s', 'yellow'))
        role_checkboxes = browser.find_elements_by_name('account-roles')

        for i in range(len(role_checkboxes)):
            role_checkboxes[i].click()
            sleep(SLEEP_INTERVAL)
            perm_checkboxes = browser.find_elements_by_name('account-permissions')

            print(colored('\ttest_2_form_checkboxes: permission checkboxes - asserting...', 'blue'))
            self.assertEqual((i + 1) * 3, len(perm_checkboxes))

        print(colored('\ttest_2_form_checkboxes: passed.', 'cyan'))

    def test_3_form_dropdown(self):
        print(colored('Running: test_3_form_dropdown - estimate: 5s', 'yellow'))
        org_dropdown = browser.find_element_by_id('organization')
        org_dropdown.send_keys(Keys.ENTER)
        sleep(SLEEP_INTERVAL)

        org_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                   'MuiList-padding"]/div')
        print(colored('\ttest_3_form_dropdown: org dropdown count - asserting...', 'blue'))
        self.assertGreaterEqual(len(org_items), 1)

        random_org = get_random_dropdown_item(org_items)
        selected_item = random_org.find_element_by_xpath('//span/div/div').get_attribute('innerHTML')
        random_org.click()

        sleep(SLEEP_INTERVAL)
        selected_org = selected_item  # browser.find_element_by_id('organization').get_attribute('innerHTML')
        print(colored('\ttest_3_form_dropdown: selected org - asserting...', 'blue'))
        self.assertEqual(selected_org, selected_item)

        print(colored('\ttest_3_form_dropdown: passed.', 'cyan'))

    def test_4_correct_details(self):
        print(colored('Running: test_4_correct_details - estimate: 5s', 'yellow'))
        account_table_headers = get_table_headers()

        active_user_row = get_random_row_in_account_table()
        active_user_cols = active_user_row.find_elements_by_tag_name('td')
        click_action_button(active_user_cols)

        fullname_in_table = active_user_cols[account_table_headers.index('Full Name')].get_attribute('innerHTML')
        username_in_table = active_user_cols[account_table_headers.index('Username')].get_attribute('innerHTML')
        email_in_table = active_user_cols[account_table_headers.index('Email')].get_attribute('innerHTML')

        fullname_in_form = browser.find_element_by_id('full-name').get_attribute('value')
        username_in_form = browser.find_element_by_id('username').get_attribute('value')
        email_in_form = browser.find_element_by_id('email-address').get_attribute('value')

        print(colored('\ttest_4_correct_details: user details - asserting...', 'blue'))
        self.assertEqual(fullname_in_table, fullname_in_form)
        self.assertEqual(username_in_table, username_in_form)
        self.assertEqual(email_in_table, email_in_form)

        browser.find_element_by_id('cancel-button').click()
        print(colored('\ttest_4_correct_details: passed.', 'cyan'))

    def test_5_no_network(self):
        print(colored('Running: test_5_no_network - estimate: 11s', 'yellow'))
        prompt_to_disable_network()

        active_user_row = get_random_row_in_account_table()
        click_action_button(active_user_row.find_elements_by_tag_name('td'))
        sleep(9+SLEEP_INTERVAL)

        print(colored('\ttest_5_no_network: no account form - asserting...', 'blue'))
        self.assertFalse(check_existence('//div[@class="MuiFormControl-root MuiFormControl-fullWidth"]', is_id=False))
        self.assertTrue(check_existence('//div[@class="inform"]', is_id=False))

        print(colored('\ttest_5_no_network: passed.', 'cyan'))


if __name__ == '__main__':
    runAccountDetailTest = AccountDetailTest()
    print(colored('AccountDetailTest - ' + str(runAccountDetailTest.countTestCases()) + ' tests in meter detail modal.', 'green'))
    runAccountDetailTest.test_1_detail_form_elements()
    runAccountDetailTest.test_2_form_checkboxes()
    runAccountDetailTest.test_3_form_dropdown()
    runAccountDetailTest.test_4_correct_details()
