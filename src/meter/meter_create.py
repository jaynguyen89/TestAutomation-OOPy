import unittest
from time import sleep
from datetime import date, datetime
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, clear_inputs, get_random_table_data,\
    pick_random_dropdown_item, click_fab_button, click_save_button


class MeterCreateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 45s', 'yellow'))
        prompt_to_disable_network()

        for i in range(3):
            print(colored('\tnew meter ' + str(i + 1), 'magenta'))
            click_fab_button()

            click_save_button()
            sleep(3*SLEEP_INTERVAL)
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving meter" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageMeter')

    @staticmethod
    def test_2_no_primary_key():
        print(colored('Running: test_2_no_primary_key - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew meter ' + str(i + 1), 'magenta'))
            click_fab_button()
            clear_inputs(['serial-number'], 'id')

            click_save_button()
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_no_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving meter" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_2_no_primary_key: passed.', 'cyan'))

    @staticmethod
    def test_3_no_device_model():
        print(colored('Running: test_3_no_device_model - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew meter ' + str(i + 1), 'magenta'))
            click_fab_button()

            browser.find_element_by_id('serial-number').send_keys('testing' + str(i + 1))
            click_save_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_3_no_device_model: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving meter" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_3_no_device_model: passed.', 'cyan'))

    @staticmethod
    def test_4_create_success():
        print(colored('Running: test_4_create_success - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\tnew meter ' + str(i + 1), 'magenta'))
            end_point = get_random_table_data('End Point')
            click_fab_button()
            serial = str(int(datetime.now().timestamp()))

            browser.find_element_by_id('meter-name').send_keys('testing name')
            browser.find_element_by_id('serial-number').send_keys(serial)
            browser.find_element_by_id('endpoint-address').send_keys(end_point)
            browser.find_element_by_id('pulse-weight').send_keys('1.23')
            browser.find_element_by_id('volume-unit').send_keys('GB')
            browser.find_element_by_id('pairing-status').send_keys('testing pairing status note')
            browser.find_element_by_id('installed-on').send_keys(date.today().strftime("%d/%m/%Y"))
            browser.find_element_by_id('activated-on').send_keys(date.today().strftime("%d/%m/%Y"))
            random_device_model = pick_random_dropdown_item('device-model')
            # random_model_value = random_device_model.find_element_by_xpath('//span/div/div').get_attribute('innerHTML')

            click_save_button()

            print(colored('\ttest_4_create_success: alert message - asserting...', 'blue'))
            assert "New meter has been saved successfully with Serial No. " + serial in browser.page_source

        print(colored('\ttest_4_create_success: passed.', 'cyan'))

    @staticmethod
    def test_5_clashed_primary_key():
        print(colored('Running: test_5_clashed_primary_key - estimate: 27s', 'yellow'))
        end_point = get_random_table_data('End Point')
        serial = get_random_table_data('Serial No.')
        click_fab_button()

        browser.find_element_by_id('meter-name').send_keys('testing name')
        browser.find_element_by_id('serial-number').send_keys(serial)
        browser.find_element_by_id('endpoint-address').send_keys(end_point)
        browser.find_element_by_id('pulse-weight').send_keys('1.23')
        browser.find_element_by_id('volume-unit').send_keys('GB')
        browser.find_element_by_id('pairing-status').send_keys('testing pairing status note')
        browser.find_element_by_id('installed-on').send_keys(date.today().strftime("%d/%m/%Y"))
        browser.find_element_by_id('activated-on').send_keys(date.today().strftime("%d/%m/%Y"))
        random_device_model = pick_random_dropdown_item('device-model')

        click_save_button()
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_5_clashed_serial: confirmation dialog - asserting...', 'blue'))
        assert "Error occurred while saving meter" in confirmation.text

        confirmation.accept()
        close_modal()
        sleep(2*SLEEP_INTERVAL)

    print(colored('\ttest_5_clashed_primary_key: passed.', 'cyan'))


if __name__ == '__main__':
    runMeterCreateTest = MeterCreateTest()
    print(colored('MeterUpdateTest - ' + str(runMeterCreateTest.countTestCases()) + ' tests in update meter.', 'green'))
    runMeterCreateTest.test_1_no_network()
    runMeterCreateTest.test_2_no_primary_key()
    runMeterCreateTest.test_3_no_device_model()
    runMeterCreateTest.test_4_create_success()
    runMeterCreateTest.test_5_clashed_primary_key()