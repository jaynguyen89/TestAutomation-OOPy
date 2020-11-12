import unittest
from time import sleep
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, close_modal, check_existence, click_delete_button, get_table_headers
from src.helper import get_random_gateway


class GatewayDeleteTest(unittest.TestCase):
    def test_1_delete_unconfirm(self):
        print(colored('Running: test_1_delete_unconfirm - estimate: 33s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            get_random_gateway()
            click_delete_button()

            browser.switch_to_alert().dismiss()
            sleep(SLEEP_INTERVAL)

            print(colored('\ttest_1_delete_unconfirm: unconfirm delete - asserting...', 'blue'))
            self.assertTrue(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))

            close_modal()

        print(colored('\ttest_1_delete_unconfirm: passed.', 'cyan'))

    @staticmethod
    def test_2_delete_confirm_no_network():
        print(colored('Running: test_2_delete_confirm_no_network - estimate: 13s', 'yellow'))
        deleted_imei = get_random_gateway()

        prompt_to_disable_network()
        click_delete_button()
        confirmation = browser.switch_to_alert()

        print(colored('\ttest_2_delete_confirm_no_network: confirm delete no network - asserting...', 'blue'))
        assert "The gateway with Imei " + deleted_imei + " will be lost permanently. Continue?" in confirmation.text

        confirmation.accept()
        sleep(9+SLEEP_INTERVAL)

        deletion_result = browser.switch_to_alert()
        print(colored('\ttest_2_delete_confirm_no_network: confirm delete no network - asserting...', 'blue'))
        assert "Error occurred while deleting gateway" in deletion_result.text

        confirmation.accept()
        sleep(SLEEP_INTERVAL)
        close_modal()

        print(colored('\ttest_2_delete_confirm_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageGateways')

    def test_3_delete_confirm_success(self):
        print(colored('Running: test_3_delete_confirm_success - estimate: 15s', 'yellow'))

        for i in range(3):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            deleted_imei = get_random_gateway()
            click_delete_button()

            browser.switch_to_alert().accept()
            sleep(2*SLEEP_INTERVAL)

            print(colored('\ttest_3_delete_confirm_success: confirm delete - asserting...', 'blue'))
            assert "The selected gateway with IMEI " + deleted_imei + " has been deleted successfully." in browser.page_source

            print(colored('\ttest_3_delete_confirm_success: check modal - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))

            gateway_table_headers = get_table_headers()
            rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
            imeis = []
            for row in rows:
                imeis.append(row.find_elements_by_tag_name('td')[gateway_table_headers.index('Imei')].get_attribute('innerHTML'))

            print(colored('\ttest_3_delete_confirm_success: check deleted imei - asserting...', 'blue'))
            assert deleted_imei not in imeis

        print(colored('\ttest_3_delete_confirm_success: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayDeleteTest = GatewayDeleteTest()
    print(colored('GatewayDeleteTest - ' + str(runGatewayDeleteTest.countTestCases()) + ' tests in delete gateway.',
                  'green'))
    runGatewayDeleteTest.test_1_delete_unconfirm()
    runGatewayDeleteTest.test_2_delete_confirm_no_network()
    runGatewayDeleteTest.test_3_delete_confirm_success()
