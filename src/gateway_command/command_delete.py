import unittest
from time import sleep
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, close_modal, check_existence, get_table_headers
from src.helper import get_random_command_and_delete


class GatewayCmdDeleteTest(unittest.TestCase):
    def test_1_delete_unconfirm(self):
        print(colored('Running: test_1_delete_unconfirm - estimate: 33s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))
            get_random_command_and_delete()

            browser.switch_to_alert().dismiss()
            sleep(SLEEP_INTERVAL)

            print(colored('\ttest_1_delete_unconfirm: unconfirm delete - asserting...', 'blue'))
            self.assertTrue(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))

            close_modal()

        print(colored('\ttest_1_delete_unconfirm: passed.', 'cyan'))

    @staticmethod
    def test_2_delete_confirm_no_network():
        print(colored('Running: test_2_delete_confirm_no_network - estimate: 13s', 'yellow'))
        prompt_to_disable_network()

        command = get_random_command_and_delete()
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_2_delete_confirm_no_network: confirm delete no network - asserting...', 'blue'))
        assert "The command " + command + " will be lost permanently. Continue?" in confirmation.text

        confirmation.accept()
        sleep(9+SLEEP_INTERVAL)

        deletion_result = browser.switch_to_alert()
        print(colored('\ttest_2_delete_confirm_no_network: confirm delete no network - asserting...', 'blue'))
        assert "Error occurred while deleting command" in deletion_result.text

        confirmation.accept()
        sleep(SLEEP_INTERVAL)
        close_modal()

        print(colored('\ttest_2_delete_confirm_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/GatewayCommand')

    def test_3_delete_confirm_success(self):
        print(colored('Running: test_3_delete_confirm_success - estimate: 15s', 'yellow'))

        for i in range(2):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))
            deleted_cmd = get_random_command_and_delete()

            browser.switch_to_alert().accept()
            sleep(2*SLEEP_INTERVAL)

            print(colored('\ttest_3_delete_confirm_success: confirm delete - asserting...', 'blue'))
            assert "The selected command has been deleted successfully." in browser.page_source

            print(colored('\ttest_3_delete_confirm_success: check modal - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))

            command_table_headers = get_table_headers()
            rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
            commands = []
            for row in rows:
                cmd_cols = row.find_elements_by_tag_name('td')
                if len(cmd_cols) > 0:
                    commands.append(row.find_elements_by_tag_name('td')[command_table_headers.index('Command')].get_attribute('innerHTML'))

            print(colored('\ttest_3_delete_confirm_success: check deleted command - asserting...', 'blue'))
            assert deleted_cmd not in commands

        print(colored('\ttest_3_delete_confirm_success: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayCmdDeleteTest = GatewayCmdDeleteTest()
    print(colored('GatewayCmdDeleteTest - ' + str(runGatewayCmdDeleteTest.countTestCases()) + ' tests in detail modal.',
                  'green'))
    runGatewayCmdDeleteTest.test_1_delete_unconfirm()
    runGatewayCmdDeleteTest.test_2_delete_confirm_no_network()
    runGatewayCmdDeleteTest.test_3_delete_confirm_success()
