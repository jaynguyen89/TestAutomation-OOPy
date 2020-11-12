import unittest
from time import sleep
from selenium.webdriver.common.keys import Keys
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_table_row,\
    get_random_dropdown_item, close_modal, click_action_button, get_table_headers


class NodeDetailTest(unittest.TestCase):
    def test_1_detail_form_elements(self):
        print(colored('Running: test_1_detail_form_elements - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))

            node_row = get_random_table_row()
            node_cols = node_row.find_elements_by_tag_name('td')
            click_action_button(node_cols)

            node_detail_form_ids = ['device-name', 'hex-address', 'dec-address', 'serial-number',
                                    'device-model', 'installed-on', 'serviced-on', 'deleted-on']

            for input_id in node_detail_form_ids:
                print(colored('\ttest_2_node_details: input "' + input_id + '" existence - asserting...', 'blue'))
                self.assertTrue(check_existence(input_id))

            close_modal()

        print(colored('\ttest_1_detail_form_elements: passed.', 'cyan'))
    
    def test_2_correct_details(self):
        print(colored('Running: test_2_correct_details - estimate: 24s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))

            node_row = get_random_table_row()
            node_cols = node_row.find_elements_by_tag_name('td')

            node_table_headers = get_table_headers()
            node_hex_in_table = node_cols[node_table_headers.index('Hex. Address')].get_attribute('innerHTML')
            node_dec_in_table = node_cols[node_table_headers.index('Dec. Address')].get_attribute('innerHTML')

            click_action_button(node_cols)

            node_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            node_hex_in_form = node_detail_form.find_element_by_id('hex-address').get_attribute('value')
            node_dec_in_form = node_detail_form.find_element_by_id('dec-address').get_attribute('value')

            print(colored('\ttest_2_node_details: is correct node - asserting...', 'blue'))
            self.assertEqual(node_hex_in_table, node_hex_in_form)
            self.assertEqual(node_dec_in_table, node_dec_in_form)

            close_modal()

        print(colored('\ttest_2_correct_details: passed.', 'cyan'))
    
    def test_3_device_model_dropdown(self):
        print(colored('Running: test_3_device_model_dropdown - estimate: 39s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))

            node_row = get_random_table_row()
            node_cols = node_row.find_elements_by_tag_name('td')
            click_action_button(node_cols)

            node_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            device_model_dropdown = node_detail_form.find_element_by_id('device-model')
            device_model_dropdown.send_keys(Keys.ENTER)
            sleep(SLEEP_INTERVAL)

            device_model_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                                'MuiList-padding"]/div')
            print(colored('\ttest_2_node_details: device models count - asserting...', 'blue'))
            self.assertGreaterEqual(len(device_model_items), 1)

            random_device_model = get_random_dropdown_item(device_model_items)
            random_model_value = random_device_model.find_element_by_xpath('//span/div/div').get_attribute('innerHTML')
            random_device_model.click()

            sleep(SLEEP_INTERVAL)
            random_model_selected = random_model_value  # browser.find_element_by_id('device-model').get_attribute('innerHTML')
            print(colored('\ttest_2_node_details: device models selected - asserting...', 'blue'))
            self.assertEqual(random_model_value, random_model_selected)

            close_modal()

        print(colored('\ttest_3_device_model_dropdown: passed.', 'cyan'))
    
    def test_4_detail_closed(self):
        print(colored('Running: test_4_detail_closed - estimate: 19s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))

            node_row = get_random_table_row()
            node_cols = node_row.find_elements_by_tag_name('td')
            click_action_button(node_cols)
            close_modal()

            print(colored('\ttest_2_node_details: modal closed - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_4_detail_closed: passed.', 'cyan'))


if __name__ == '__main__':
    runNodeDetailTest = NodeDetailTest()
    print(colored('NodeDetailTest - ' + str(runNodeDetailTest.countTestCases()) + ' tests in detail modal.', 'green'))
    runNodeDetailTest.test_1_detail_form_elements()
    runNodeDetailTest.test_2_correct_details()
    runNodeDetailTest.test_3_device_model_dropdown()
    runNodeDetailTest.test_4_detail_closed()
