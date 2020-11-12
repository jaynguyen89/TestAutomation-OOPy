import unittest
from time import sleep
from datetime import date

from selenium.webdriver.common.keys import Keys
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, get_random_dropdown_item, clear_inputs, click_update_button
from src.helper import get_random_gateway, get_back_previously_updated_gateway


class GatewayUpdateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 11s', 'yellow'))
        get_random_gateway()
        prompt_to_disable_network()
        click_update_button()
        sleep(9+SLEEP_INTERVAL)

        confirmation = browser.switch_to_alert()

        print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
        assert "Error occurred while updating gateway" in confirmation.text

        confirmation.accept()
        close_modal()

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageGateways')

    @staticmethod
    def test_2_missing_primary_key():
        print(colored('Running: test_2_missing_primary_key - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            get_random_gateway()
            clear_inputs(['gateway-imei'], 'id')
            click_update_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_missing_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while updating gateway" in confirmation.text

            confirmation.accept()
            close_modal()

        print(colored('\ttest_2_missing_primary_key: passed.', 'cyan'))

    def test_3_device_model(self):
        print(colored('Running: test_3_device_model - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            updated_imei = get_random_gateway()
            gateway_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            device_model_dropdown = gateway_detail_form.find_element_by_id('device-model')
            device_model_dropdown.send_keys(Keys.ENTER)
            sleep(SLEEP_INTERVAL)
            device_model_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                                'MuiList-padding"]/li')
            random_device_model = get_random_dropdown_item(device_model_items)
            random_device_model.click()
            click_update_button()

            print(colored('\ttest_3_device_model: confirm update - asserting...', 'blue'))
            assert "The selected gateway with IMEI " + updated_imei + " has been updated successfully." in browser.page_source

            get_back_previously_updated_gateway(updated_imei)
            close_modal()

        print(colored('\ttest_3_device_model: passed.', 'cyan'))

    @staticmethod
    def test_4_dates():
        print(colored('Running: test_4_dates - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            updated_imei = get_random_gateway()

            installed_on_input = browser.find_element_by_id('installed-on')
            created_on_input = browser.find_element_by_id('created-on')
            updated_on_input = browser.find_element_by_id('updated-on')

            installed_on_input.send_keys(date.today().strftime("%d/%m/%Y"))
            created_on_input.send_keys(date.today().strftime("%d/%m/%Y"))
            updated_on_input.send_keys(date.today().strftime("%d/%m/%Y"))

            sleep(SLEEP_INTERVAL)
            click_update_button()

            print(colored('\ttest_4_dates: confirm delete - asserting...', 'blue'))
            assert "The selected gateway with IMEI " + updated_imei + " has been updated successfully." in browser.page_source

            # get_back_previously_updated_gateway(updated_imei)
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
        print(colored('Running: test_6_input_validations - estimate: 57s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            updated_imei = get_random_gateway()

        # the app need update: verify inputs


if __name__ == '__main__':
    runGatewayUpdateTest = GatewayUpdateTest()
    print(colored('GatewayUpdateTest - ' + str(runGatewayUpdateTest.countTestCases()) + ' tests in update gateway.',
                  'green'))
    runGatewayUpdateTest.test_1_no_network()
    runGatewayUpdateTest.test_2_missing_primary_key()
    runGatewayUpdateTest.test_3_device_model()
    # runGatewayUpdateTest.test_4_dates()
    # runGatewayUpdateTest.test_5_input_validations()
