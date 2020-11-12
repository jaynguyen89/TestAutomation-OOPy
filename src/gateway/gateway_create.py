import unittest
from datetime import datetime
from time import sleep

from selenium.webdriver.common.keys import Keys
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, clear_inputs, get_random_table_data, \
    click_fab_button, click_save_button, get_random_dropdown_item


class GatewayCreateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 48s', 'yellow'))
        prompt_to_disable_network()
        click_fab_button()

        click_save_button()
        sleep(9+SLEEP_INTERVAL)
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
        assert "Error occurred while saving gateway" in confirmation.text

        confirmation.accept()

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        browser.refresh()
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageGateways')

    @staticmethod
    def test_2_no_primary_key():
        print(colored('Running: test_2_no_primary_key - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew gateway ' + str(i + 1), 'magenta'))
            click_fab_button()
            clear_inputs(['gateway-imei'], 'id')

            click_save_button()
            sleep(3*SLEEP_INTERVAL)
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_no_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving gateway" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_2_no_primary_key: passed.', 'cyan'))

    @staticmethod
    def test_3_no_device_model():
        print(colored('Running: test_3_no_device_model - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew gateway ' + str(i + 1), 'magenta'))
            click_fab_button()

            browser.find_element_by_id('gateway-imei').send_keys('testing' + str(i + 1))
            click_save_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_3_no_device_model: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving gateway" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_3_no_device_model: passed.', 'cyan'))

    @staticmethod
    def test_4_create_success():
        print(colored('Running: test_4_create_success - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\tnew gateway ' + str(i + 1), 'magenta'))
            click_fab_button()

            imei = str(int(datetime.now().timestamp())) + "-" + str(i + 1)
            browser.find_element_by_id('gateway-imei').send_keys(imei)
            browser.find_element_by_id('gateway-name').send_keys('test name')
            browser.find_element_by_id('phone-number').send_keys('test phone')
            browser.find_element_by_id('hex-address').send_keys('hex address')
            browser.find_element_by_id('dec-address').send_keys('dec address')
            browser.find_element_by_id('ip-address').send_keys('ip address')
            browser.find_element_by_id('software-version').send_keys('sw version')
            browser.find_element_by_id('firmware-version').send_keys('fw version')
            browser.find_element_by_id('sim-serial').send_keys('sim serial')
            browser.find_element_by_id('sim-puk').send_keys('sim puk')

            gateway_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
            device_model_dropdown = gateway_detail_form.find_element_by_id('device-model')
            device_model_dropdown.send_keys(Keys.ENTER)
            sleep(SLEEP_INTERVAL)
            device_model_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                                'MuiList-padding"]/li')
            random_device_model = get_random_dropdown_item(device_model_items)
            random_device_model.click()

            click_save_button()

            print(colored('\ttest_4_create_success: alert message - asserting...', 'blue'))
            assert "New gateway has been created successfully with IMEI " + imei in browser.page_source

        print(colored('\ttest_4_create_success: passed.', 'cyan'))

    @staticmethod
    def test_5_clashed_primary_key():
        print(colored('Running: test_5_clashed_primary_key - estimate: 27s', 'yellow'))

        imei = get_random_table_data('Imei')
        click_fab_button()

        browser.find_element_by_id('gateway-imei').send_keys(imei)
        browser.find_element_by_id('gateway-name').send_keys('test name')
        browser.find_element_by_id('phone-number').send_keys('test phone')
        browser.find_element_by_id('hex-address').send_keys('hex address')
        browser.find_element_by_id('dec-address').send_keys('dec address')
        browser.find_element_by_id('ip-address').send_keys('ip address')
        browser.find_element_by_id('software-version').send_keys('sw version')
        browser.find_element_by_id('firmware-version').send_keys('fw version')
        browser.find_element_by_id('sim-serial').send_keys('sim serial')
        browser.find_element_by_id('sim-puk').send_keys('sim puk')

        gateway_detail_form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
        device_model_dropdown = gateway_detail_form.find_element_by_id('device-model')
        device_model_dropdown.send_keys(Keys.ENTER)
        sleep(SLEEP_INTERVAL)
        device_model_items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                                            'MuiList-padding"]/li')
        random_device_model = get_random_dropdown_item(device_model_items)
        random_device_model.click()

        click_save_button()
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_5_clashed_serial: confirmation dialog - asserting...', 'blue'))
        assert "Error occurred while saving gateway" in confirmation.text

        confirmation.accept()
        close_modal()
        sleep(2*SLEEP_INTERVAL)

    print(colored('\ttest_5_clashed_primary_key: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayCreateTest = GatewayCreateTest()
    print(colored('GatewayCreateTest - ' + str(runGatewayCreateTest.countTestCases()) + ' tests in update gateway.',
                  'green'))
    runGatewayCreateTest.test_1_no_network()
    runGatewayCreateTest.test_2_no_primary_key()
    runGatewayCreateTest.test_3_no_device_model()
    # runGatewayCreateTest.test_4_create_success()
    runGatewayCreateTest.test_5_clashed_primary_key()
