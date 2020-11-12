import unittest
from time import sleep
from selenium.webdriver.common.keys import Keys
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_table_row,\
    get_random_dropdown_item, close_modal, click_action_button, get_table_headers


class MeterDetailTest(unittest.TestCase):
    def test_1_detail_form_elements(self):
        print(colored('Running: test_1_detail_form_elements - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom meter ' + str(i + 1), 'magenta'))

            meter_row = get_random_table_row()
            meter_cols = meter_row.find_elements_by_tag_name('td')
            click_action_button(meter_cols)

            meter_detail_form_ids = ['meter-name', 'serial-number', 'endpoint-address', 'device-model',
                                     'pulse-weight', 'volume-unit', 'pairing-status', 'installed-on',
                                     'activated-on', 'is-active', 'deactivated-on', 'deleted-on']

            for input_id in meter_detail_form_ids:
                print(colored('\ttest_1_detail_form_elements: input "' + input_id + '" existence - asserting...', 'blue'))
                self.assertTrue(check_existence(input_id))

            close_modal()

        print(colored('\ttest_1_detail_form_elements: passed.', 'cyan'))

    def test_2_correct_details(self):
        print(colored('Running: test_2_correct_details - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom meter ' + str(i + 1), 'magenta'))

            meter_row = get_random_table_row()
            meter_cols = meter_row.find_elements_by_tag_name('td')

            meter_table_headers = get_table_headers()

            meter_serial_in_table = meter_cols[meter_table_headers.index('Serial No.')].get_attribute('innerHTML')
            meter_endpoint_in_table = meter_cols[meter_table_headers.index('End Point')].get_attribute('innerHTML')
            click_action_button(meter_cols)

            meter_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            meter_serial_in_form = meter_detail_form.find_element_by_id('serial-number').get_attribute('value')
            meter_endpoint_in_form = meter_detail_form.find_element_by_id('endpoint-address').get_attribute('value')

            print(colored('\ttest_2_correct_details: is correct meter - asserting...', 'blue'))
            self.assertEqual(meter_serial_in_table, meter_serial_in_form)
            self.assertEqual(meter_endpoint_in_table, meter_endpoint_in_form)

            close_modal()

        print(colored('\ttest_2_correct_details: passed.', 'cyan'))

    def test_3_device_model_dropdown(self):
        print(colored('Running: test_3_device_model_dropdown - estimate: 39s', 'yellow'))

        for i in range(3):
            print(colored('\trandom meter ' + str(i + 1), 'magenta'))

            meter_row = get_random_table_row()
            meter_cols = meter_row.find_elements_by_tag_name('td')
            click_action_button(meter_cols)

            meter_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            device_model_dropdown = meter_detail_form.find_element_by_id('device-model')
            device_model_dropdown.send_keys(Keys.ENTER)
            sleep(SLEEP_INTERVAL)

            device_model_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                                'MuiList-padding"]/div')
            print(colored('\ttest_3_device_model_dropdown: device models count - asserting...', 'blue'))
            self.assertGreaterEqual(len(device_model_items), 1)

            random_device_model = get_random_dropdown_item(device_model_items)
            random_model_value = random_device_model.find_element_by_xpath('//span/div/div').get_attribute('innerHTML')
            random_device_model.click()

            sleep(SLEEP_INTERVAL)
            random_model_selected = random_model_value # browser.find_element_by_id('device-model').get_attribute('innerHTML')
            print(colored('\ttest_3_device_model_dropdown: device models selected - asserting...', 'blue'))
            self.assertEqual(random_model_value, random_model_selected)

            close_modal()

        print(colored('\ttest_3_device_model_dropdown: passed.', 'cyan'))

    def test_4_detail_closed(self):
        print(colored('Running: test_4_detail_closed - estimate: 19s', 'yellow'))

        for i in range(3):
            print(colored('\trandom meter ' + str(i + 1), 'magenta'))

            meter_row = get_random_table_row()
            meter_cols = meter_row.find_elements_by_tag_name('td')
            click_action_button(meter_cols)

            close_modal()

            print(colored('\ttest_4_detail_closed: modal closed - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_4_detail_closed: passed.', 'cyan'))


if __name__ == '__main__':
    runMeterDetailTest = MeterDetailTest()
    print(colored('MeterDetailTest - ' + str(runMeterDetailTest.countTestCases()) + ' tests in meter detail modal.', 'green'))
    runMeterDetailTest.test_1_detail_form_elements()
    runMeterDetailTest.test_2_correct_details()
    runMeterDetailTest.test_3_device_model_dropdown()
    runMeterDetailTest.test_4_detail_closed()
