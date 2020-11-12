import unittest
from time import sleep
from datetime import datetime
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, clear_inputs, get_random_table_data,\
    pick_random_dropdown_item, click_fab_button, click_save_button


class GatewayCmdCreateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 45s', 'yellow'))
        prompt_to_disable_network()

        for i in range(3):
            print(colored('\tnew command ' + str(i + 1), 'magenta'))
            click_fab_button()

            click_save_button()
            sleep(3*SLEEP_INTERVAL)
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving command" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/GatewayCommand')

    @staticmethod
    def test_2_no_primary_key():
        print(colored('Running: test_2_no_primary_key - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew command ' + str(i + 1), 'magenta'))
            click_fab_button()
            clear_inputs(['command-syntax'], 'id')

            click_save_button()
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_no_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving command" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_2_no_primary_key: passed.', 'cyan'))

    @staticmethod
    def test_3_no_command_type():
        print(colored('Running: test_3_no_command_model - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew command ' + str(i + 1), 'magenta'))
            click_fab_button()

            browser.find_element_by_id('command-syntax').send_keys('testing' + str(i + 1))
            click_save_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_3_no_command_model: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving command" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_3_no_command_model: passed.', 'cyan'))

    @staticmethod
    def test_4_create_success():
        print(colored('Running: test_4_create_success - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\tnew command ' + str(i + 1), 'magenta'))
            click_fab_button()

            browser.find_element_by_id('command-name').send_keys('test name ' + str(i + 1))
            pick_random_dropdown_item('device-model')
            pick_random_dropdown_item('command-type')
            browser.find_element_by_id('command-syntax').send_keys('syntax ' + str(int(datetime.now().timestamp())))
            browser.find_element_by_id('command-description').send_keys('command description testing')

            click_save_button()

            print(colored('\ttest_4_create_success: alert message - asserting...', 'blue'))
            assert "New command has been created successfully." in browser.page_source

        print(colored('\ttest_4_create_success: passed.', 'cyan'))

    @staticmethod
    def test_5_clashed_primary_key():
        print(colored('Running: test_5_clashed_primary_key - estimate: 27s', 'yellow'))

        command = get_random_table_data('Command')
        click_fab_button()

        browser.find_element_by_id('command-name').send_keys('test name')
        browser.find_element_by_id('command-syntax').send_keys(command)
        pick_random_dropdown_item('device-model')
        pick_random_dropdown_item('command-type')
        browser.find_element_by_id('command-description').send_keys('command description testing')

        click_save_button()
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_5_clashed_primary_key: confirmation dialog - asserting...', 'blue'))
        assert "Error occurred while saving command" in confirmation.text

        confirmation.accept()
        close_modal()
        sleep(2*SLEEP_INTERVAL)

    print(colored('\ttest_5_clashed_primary_key: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayCmdCreateTest = GatewayCmdCreateTest()
    print(colored('GatewayCmdCreateTest - ' + str(runGatewayCmdCreateTest.countTestCases()) + ' tests in detail modal.',
                  'green'))
    runGatewayCmdCreateTest.test_1_no_network()
    runGatewayCmdCreateTest.test_2_no_primary_key()
    runGatewayCmdCreateTest.test_3_no_command_type()
    runGatewayCmdCreateTest.test_4_create_success()
    # runGatewayCmdCreateTest.test_5_clashed_primary_key()
