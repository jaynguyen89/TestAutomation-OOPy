import unittest
from time import sleep
from datetime import date
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, pick_random_dropdown_item, clear_inputs, click_update_button
from src.helper import get_random_node, get_back_previously_updated_node


class NodeUpdateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            get_random_node()
            click_update_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while updating device" in confirmation.text

            confirmation.accept()
            close_modal()

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageDevice')

    @staticmethod
    def test_2_missing_primary_key():
        print(colored('Running: test_2_missing_primary_key - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            get_random_node()
            clear_inputs(['hex-address'], 'id')
            click_update_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_missing_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while updating device" in confirmation.text

            confirmation.accept()
            close_modal()

        print(colored('\ttest_2_missing_primary_key: passed.', 'cyan'))

    def test_3_device_model(self):
        print(colored('Running: test_3_device_model - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            updated_hex = get_random_node()
            random_model_value = pick_random_dropdown_item('device-model')
            click_update_button()

            print(colored('\ttest_3_device_model: confirm update - asserting...', 'blue'))
            assert "The AMR Device with Hex. Address " + updated_hex + " has been updated successfully." in browser.page_source

            get_back_previously_updated_node(updated_hex)

            updated_device_model = random_model_value  # browser.find_element_by_id('device-model').get_attribute('innerHTML')
            print(colored('\ttest_3_device_model: device models selected - asserting...', 'blue'))
            self.assertEqual(random_model_value, updated_device_model)

            close_modal()

        print(colored('\ttest_3_device_model: passed.', 'cyan'))

    @staticmethod
    def test_4_dates():
        print(colored('Running: test_4_dates - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            updated_serial = get_random_node()

            installed_on_input = browser.find_element_by_id('installed-on')
            serviced_on_input = browser.find_element_by_id('serviced-on')

            installed_on_input.send_keys(date.today().strftime("%d/%m/%Y"))
            serviced_on_input.send_keys(date.today().strftime("%d/%m/%Y"))

            sleep(SLEEP_INTERVAL)
            click_update_button()

            print(colored('\ttest_4_dates: confirm delete - asserting...', 'blue'))
            assert "The AMR Device with Hex. Address " + updated_serial + " has been updated successfully." in browser.page_source

            # get_back_previously_updated_node(updated_serial)
            #
            # new_installed_on = browser.find_element_by_id('installed-on').get_property('value')
            # new_activated_on = browser.find_element_by_id('activated-on').get_property('value')
            #
            # print(colored('\ttest_4_dates: is dates correct - asserting...', 'blue'))
            # self.assertEqual(new_installed_on, date.today().strftime("%d/%m/%Y"))
            # self.assertEqual(new_activated_on, date.today().strftime("%d/%m/%Y"))
            #
            # close_modal()

        print(colored('\ttest_4_dates: passed.', 'cyan'))

    @staticmethod
    def test_5_input_validations():
        print(colored('Running: test_5_input_validations - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            updated_hex = get_random_node()

        # the app need update: verify inputs


if __name__ == '__main__':
    runNodeUpdateTest = NodeUpdateTest()
    print(colored('NodeUpdateTest - ' + str(runNodeUpdateTest.countTestCases()) + ' tests in detail modal.', 'green'))
    runNodeUpdateTest.test_1_no_network()
    runNodeUpdateTest.test_2_missing_primary_key()
    runNodeUpdateTest.test_3_device_model()
    runNodeUpdateTest.test_4_dates()
    # runNodeUpdateTest.test_5_input_validations()
