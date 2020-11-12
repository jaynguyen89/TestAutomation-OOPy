import unittest
from time import sleep
from datetime import date, datetime
from termcolor import colored
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from src.utility import SLEEP_INTERVAL, browser, close_modal, clear_inputs, get_random_table_data,\
    pick_random_dropdown_item, click_fab_button, click_save_button


class NodeCreateTest(unittest.TestCase):
    @staticmethod
    def test_1_no_network():
        print(colored('Running: test_1_no_network - estimate: 45s', 'yellow'))
        prompt_to_disable_network()

        for i in range(3):
            print(colored('\tnew node ' + str(i + 1), 'magenta'))
            click_fab_button()

            click_save_button()
            sleep(3*SLEEP_INTERVAL)
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_1_no_network: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving device" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_1_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageDevice')

    @staticmethod
    def test_2_no_primary_key():
        print(colored('Running: test_2_no_primary_key - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew node ' + str(i + 1), 'magenta'))
            click_fab_button()
            clear_inputs(['hex-address'], 'id')

            click_save_button()
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_no_primary_key: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving device" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_2_no_primary_key: passed.', 'cyan'))

    @staticmethod
    def test_3_no_device_model():
        print(colored('Running: test_3_no_device_model - estimate: 45s', 'yellow'))

        for i in range(3):
            print(colored('\tnew node ' + str(i + 1), 'magenta'))
            click_fab_button()

            browser.find_element_by_id('hex-address').send_keys('testing' + str(i + 1))
            click_save_button()

            confirmation = browser.switch_to_alert()

            print(colored('\ttest_3_no_device_model: confirmation dialog - asserting...', 'blue'))
            assert "Error occurred while saving device" in confirmation.text

            confirmation.accept()
            close_modal()
            sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_3_no_device_model: passed.', 'cyan'))

    @staticmethod
    def test_4_create_success():
        print(colored('Running: test_4_create_success - estimate: 27s', 'yellow'))

        for i in range(3):
            print(colored('\tnew node ' + str(i + 1), 'magenta'))
            click_fab_button()

            browser.find_element_by_id('device-name').send_keys('test name ' + str(i + 1))
            browser.find_element_by_id('hex-address').send_keys(str(int(datetime.now().timestamp())))
            browser.find_element_by_id('dec-address').send_keys('decimal' + str(i + 1))
            browser.find_element_by_id('serial-number').send_keys('test serial ' + str(i + 1))
            browser.find_element_by_id('installed-on').send_keys(date.today().strftime("%d/%m/%Y"))
            browser.find_element_by_id('serviced-on').send_keys(date.today().strftime("%d/%m/%Y"))
            random_device_model = pick_random_dropdown_item('device-model')
            # random_model_value = random_device_model.find_element_by_xpath('//span/div/div').get_attribute('innerHTML')

            click_save_button()

            print(colored('\ttest_4_create_success: alert message - asserting...', 'blue'))
            assert "New AMR Device has been saved successfully with Hex. Address" in browser.page_source

        print(colored('\ttest_4_create_success: passed.', 'cyan'))

    @staticmethod
    def test_5_clashed_primary_key():
        print(colored('Running: test_5_clashed_primary_key - estimate: 27s', 'yellow'))

        hex = get_random_table_data('Hex. Address')
        click_fab_button()

        browser.find_element_by_id('device-name').send_keys('test name')
        browser.find_element_by_id('hex-address').send_keys(hex)
        browser.find_element_by_id('dec-address').send_keys('decimal')
        browser.find_element_by_id('serial-number').send_keys('test serial')
        browser.find_element_by_id('installed-on').send_keys(date.today().strftime("%d/%m/%Y"))
        browser.find_element_by_id('serviced-on').send_keys(date.today().strftime("%d/%m/%Y"))
        random_device_model = pick_random_dropdown_item('device-model')

        click_save_button()
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_5_clashed_primary_key: confirmation dialog - asserting...', 'blue'))
        assert "Error occurred while saving device" in confirmation.text

        confirmation.accept()
        close_modal()
        sleep(2*SLEEP_INTERVAL)

    print(colored('\ttest_5_clashed_primary_key: passed.', 'cyan'))


if __name__ == '__main__':
    runNodeCreateTest = NodeCreateTest()
    print(colored('NodeCreateTest - ' + str(runNodeCreateTest.countTestCases()) + ' tests in detail modal.', 'green'))
    runNodeCreateTest.test_1_no_network()
    runNodeCreateTest.test_2_no_primary_key()
    runNodeCreateTest.test_3_no_device_model()
    runNodeCreateTest.test_4_create_success()
    runNodeCreateTest.test_5_clashed_primary_key()
