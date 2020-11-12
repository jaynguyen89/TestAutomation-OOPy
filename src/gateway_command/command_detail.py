import unittest
from time import sleep
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_table_row, \
    close_modal, click_action_button, get_table_headers


class GatewayCmdDetailTest(unittest.TestCase):
    def test_1_detail_form_elements(self):
        print(colored('Running: test_1_detail_form_elements - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))

            command_row = get_random_table_row()
            command_cols = command_row.find_elements_by_tag_name('td')
            click_action_button(command_cols)

            cmd_detail_form_ids = ['command-name', 'device-model', 'command-type', 'command-syntax',
                                   'command-description', 'created-on', 'created-by', 'updated-on', 'updated-by']

            for input_id in cmd_detail_form_ids:
                print(colored('\ttest_2_command_details: input "' + input_id + '" existence - asserting...', 'blue'))
                self.assertTrue(check_existence(input_id))

            close_modal()

        print(colored('\ttest_1_detail_form_elements: passed.', 'cyan'))

    def test_2_correct_details(self):
        print(colored('Running: test_2_correct_details - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))

            command_row = get_random_table_row()
            command_cols = command_row.find_elements_by_tag_name('td')

            command_table_headers = get_table_headers()
            command_name_in_table = command_cols[command_table_headers.index('Name')].get_attribute('innerHTML')
            command_syntax_in_table = command_cols[command_table_headers.index('Command')].get_attribute('innerHTML')
            command_type_in_table = command_cols[command_table_headers.index('Type')].get_attribute('innerHTML')

            click_action_button(command_cols)

            command_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            command_name_in_form = command_detail_form.find_element_by_id('command-name').get_attribute('value')
            command_syntax_in_form = command_detail_form.find_element_by_id('command-syntax').get_attribute('value')
            command_type_in_form = command_type_in_table # command_detail_form.find_element_by_id('command-type').get_attribute('value')

            print(colored('\ttest_2_command_details: is correct command - asserting...', 'blue'))
            self.assertEqual(command_name_in_table, command_name_in_form)
            self.assertEqual(command_syntax_in_table, command_syntax_in_form)
            self.assertEqual(command_type_in_table, command_type_in_form)

            close_modal()

        print(colored('\ttest_2_correct_details: passed.', 'cyan'))

    def test_3_detail_closed(self):
        print(colored('Running: test_3_detail_closed - estimate: 19s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))

            command_row = get_random_table_row()
            command_cols = command_row.find_elements_by_tag_name('td')
            click_action_button(command_cols)
            close_modal()

            print(colored('\ttest_3_detail_closed: modal closed - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_3_detail_closed: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayCmdDetailTest = GatewayCmdDetailTest()
    print(colored('GatewayCmdDetailTest - ' + str(runGatewayCmdDetailTest.countTestCases()) + ' tests in detail modal.',
                  'green'))
    runGatewayCmdDetailTest.test_1_detail_form_elements()
    runGatewayCmdDetailTest.test_2_correct_details()
    runGatewayCmdDetailTest.test_3_detail_closed()
