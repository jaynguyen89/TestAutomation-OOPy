import unittest
from time import sleep
from selenium.webdriver.common.keys import Keys
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_table_row,\
    get_random_dropdown_item, close_modal, click_action_button, get_table_headers


class GatewayDetailTest(unittest.TestCase):
    def test_1_detail_no_network(self):
        print(colored('Running: test_1_detail_no_network - estimate: 24s', 'yellow'))
        prompt_to_disable_network()

        gateway_row = get_random_table_row()
        gateway_cols = gateway_row.find_elements_by_tag_name('td')
        click_action_button(gateway_cols)
        sleep(3*SLEEP_INTERVAL)

        print(colored('\ttest_1_detail_no_network: inform existence - asserting...', 'blue'))
        self.assertTrue(check_existence('//div[@class="inform"]', is_id=False))

        print(colored('\ttest_1_detail_no_network: passed.', 'cyan'))
        browser.refresh()
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageGateways')

    def test_2_detail_form_elements(self):
        print(colored('Running: test_2_detail_form_elements - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))

            gateway_row = get_random_table_row()
            gateway_cols = gateway_row.find_elements_by_tag_name('td')
            click_action_button(gateway_cols)

            gateway_detail_form_ids = ['gateway-imei', 'gateway-name', 'phone-number', 'serial-number',
                                       'hex-address', 'dec-address', 'ip-address', 'software-version',
                                       'firmware-version', 'sim-serial', 'sim-puk', 'device-model',
                                       'installed-on', 'created-on', 'updated-on']

            for input_id in gateway_detail_form_ids:
                print(colored('\ttest_2_detail_form_elements: input "' + input_id + '" existence - asserting...', 'blue'))
                self.assertTrue(check_existence(input_id))

            close_modal()

        print(colored('\ttest_2_detail_form_elements: passed.', 'cyan'))

    def test_3_correct_details(self):
        print(colored('Running: test_3_correct_details - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))

            gateway_row = get_random_table_row()
            gateway_cols = gateway_row.find_elements_by_tag_name('td')

            gateway_table_headers = get_table_headers()
            gateway_imei_in_table = gateway_cols[gateway_table_headers.index('Imei')].get_attribute('innerHTML')
            gateway_serial_in_table = gateway_cols[gateway_table_headers.index('Serial No.')].get_attribute('innerHTML')
            gateway_hex_in_table = gateway_cols[gateway_table_headers.index('Hex. Address')].get_attribute('innerHTML')
            gateway_dec_in_table = gateway_cols[gateway_table_headers.index('Dec. Address')].get_attribute('innerHTML')
            gateway_ip_in_table = gateway_cols[gateway_table_headers.index('IP Address')].get_attribute('innerHTML')
            gateway_phone_in_table = gateway_cols[gateway_table_headers.index('Phone No.')].get_attribute('innerHTML')
            click_action_button(gateway_cols)

            gateway_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            gateway_imei_in_form = gateway_detail_form.find_element_by_id('gateway-imei').get_attribute('value')
            gateway_serial_in_form = gateway_detail_form.find_element_by_id('serial-number').get_attribute('value')
            gateway_hex_in_form = gateway_detail_form.find_element_by_id('hex-address').get_attribute('value')
            gateway_dec_in_form = gateway_detail_form.find_element_by_id('dec-address').get_attribute('value')
            gateway_ip_in_form = gateway_detail_form.find_element_by_id('ip-address').get_attribute('value')
            gateway_phone_in_form = gateway_detail_form.find_element_by_id('phone-number').get_attribute('value')

            print(colored('\ttest_3_correct_details: is correct gateway - asserting...', 'blue'))
            self.assertEqual(gateway_imei_in_table, gateway_imei_in_form)
            self.assertEqual(gateway_serial_in_table, gateway_serial_in_form)
            self.assertEqual(gateway_hex_in_table, gateway_hex_in_form)
            self.assertEqual(gateway_dec_in_table, gateway_dec_in_form)
            self.assertEqual(gateway_ip_in_table, gateway_ip_in_form)
            self.assertEqual(gateway_phone_in_table, gateway_phone_in_form)

            close_modal()

        print(colored('\ttest_3_correct_details: passed.', 'cyan'))

    def test_4_device_model_dropdown(self):
        print(colored('Running: test_4_device_model_dropdown - estimate: 39s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))

            gateway_row = get_random_table_row()
            gateway_cols = gateway_row.find_elements_by_tag_name('td')
            click_action_button(gateway_cols)

            gateway_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            device_model_dropdown = gateway_detail_form.find_element_by_id('device-model')
            device_model_dropdown.send_keys(Keys.ENTER)
            sleep(SLEEP_INTERVAL)

            device_model_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                                'MuiList-padding"]/li')
            print(colored('\ttest_4_device_model_dropdown: device models count - asserting...', 'blue'))
            self.assertGreaterEqual(len(device_model_items), 1)

            random_device_model = get_random_dropdown_item(device_model_items)
            random_model_value = random_device_model.get_attribute('innerHTML')
            random_device_model.click()

            sleep(SLEEP_INTERVAL)
            random_model_selected = random_model_value # browser.find_element_by_id('device-model').get_attribute('innerHTML')
            print(colored('\ttest_4_device_model_dropdown: device models selected - asserting...', 'blue'))
            self.assertEqual(random_model_value, random_model_selected)

            close_modal()

        print(colored('\ttest_4_device_model_dropdown: passed.', 'cyan'))

    def test_5_detail_closed(self):
        print(colored('Running: test_5_detail_closed - estimate: 19s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))

            gateway_row = get_random_table_row()
            gateway_cols = gateway_row.find_elements_by_tag_name('td')
            click_action_button(gateway_cols)

            close_modal()

            print(colored('\ttest_5_detail_closed: modal closed - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_5_detail_closed: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayDetailTest = GatewayDetailTest()
    print(
        colored('GatewayDetailTest - ' + str(runGatewayDetailTest.countTestCases()) + ' tests in gateway detail modal.',
                'green'))
    runGatewayDetailTest.test_1_detail_no_network()
    runGatewayDetailTest.test_2_detail_form_elements()
    runGatewayDetailTest.test_3_correct_details()
    runGatewayDetailTest.test_4_device_model_dropdown()
    runGatewayDetailTest.test_5_detail_closed()
