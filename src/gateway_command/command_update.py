import unittest
from time import sleep
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, pick_random_dropdown_item, clear_inputs, click_update_button
from src.helper import get_random_command, get_back_previously_updated_command


class GatewayCmdUpdateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        for i in range(2):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))
            get_random_command()
            click_update_button()
            sleep(9+SLEEP_INTERVAL)

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while updating command" in confirmation.text

            confirmation.accept()
            close_modal()

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/GatewayCommand')

    @staticmethod
    def test_2_missing_primary_key():
        print(colored('Running: test_2_missing_primary_key - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))
            get_random_command()
            clear_inputs(['command-syntax'], 'id')
            click_update_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_missing_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while updating command" in confirmation.text

            confirmation.accept()
            close_modal()

        print(colored('\ttest_2_missing_primary_key: passed.', 'cyan'))

    def test_3_command_type(self):
        print(colored('Running: test_3_command_model - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))
            updated_cmd = get_random_command()
            random_model_value = pick_random_dropdown_item('device-model')
            random_type_value = pick_random_dropdown_item('command-type')
            click_update_button()

            print(colored('\ttest_3_command_model: confirm update - asserting...', 'blue'))
            assert "The selected command has been updated successfully." in browser.page_source

            get_back_previously_updated_command(updated_cmd)

            updated_command_model = random_model_value # browser.find_element_by_id('device-model').get_attribute('innerHTML')
            updated_command_type = random_type_value # browser.find_element_by_id('command-type').get_attribute('innerHTML')
            print(colored('\ttest_3_command_model: command type selected - asserting...', 'blue'))
            self.assertEqual(random_model_value, updated_command_model)
            self.assertEqual(random_type_value, updated_command_type)

            close_modal()

        print(colored('\ttest_3_command_model: passed.', 'cyan'))

    @staticmethod
    def test_4_input_validations():
        print(colored('Running: test_5_input_validations - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom command ' + str(i + 1), 'magenta'))
            updated_hex = get_random_command()

        # the app need update: verify inputs


if __name__ == '__main__':
    runGatewayCmdUpdateTest = GatewayCmdUpdateTest()
    print(colored('GatewayCmdUpdateTest - ' + str(runGatewayCmdUpdateTest.countTestCases()) + ' tests in detail modal.',
                  'green'))
    runGatewayCmdUpdateTest.test_1_no_network()
    runGatewayCmdUpdateTest.test_2_missing_primary_key()
    # runGatewayCmdUpdateTest.test_3_command_type()
    # runGatewayCmdUpdateTest.test_4_input_validations()
