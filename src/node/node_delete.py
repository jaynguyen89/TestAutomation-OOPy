import unittest
from time import sleep
from src.root import prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored
from src.utility import SLEEP_INTERVAL, browser, close_modal, check_existence, get_table_headers
from src.helper import get_random_node_and_delete


class NodeDeleteTest(unittest.TestCase):
    def test_1_delete_unconfirm(self):
        print(colored('Running: test_1_delete_unconfirm - estimate: 33s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            get_random_node_and_delete()

            browser.switch_to_alert().dismiss()
            sleep(SLEEP_INTERVAL)

            print(colored('\ttest_1_delete_unconfirm: unconfirm delete - asserting...', 'blue'))
            self.assertTrue(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))

            close_modal()

        print(colored('\ttest_1_delete_unconfirm: passed.', 'cyan'))

    @staticmethod
    def test_2_delete_confirm_no_network():
        print(colored('Running: test_2_delete_confirm_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        for i in range(2):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            deleted_hex = get_random_node_and_delete()
            sleep(9+SLEEP_INTERVAL)
            confirmation = browser.switch_to_alert()

            print(colored('\ttest_2_delete_confirm_no_network: confirm delete no network - asserting...', 'blue'))
            assert "The device with Hex. Address " + deleted_hex + " will be lost permanently. Continue?" in confirmation.text

            confirmation.accept()
            sleep(2*SLEEP_INTERVAL)

            deletion_result = browser.switch_to_alert()
            print(colored('\ttest_2_delete_confirm_no_network: confirm delete no network - asserting...', 'blue'))
            assert "Error occurred while deleting device" in deletion_result.text

            confirmation.accept()
            sleep(SLEEP_INTERVAL)
            close_modal()

        print(colored('\ttest_2_delete_confirm_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageDevice')

    def test_3_delete_confirm_success(self):
        print(colored('Running: test_3_delete_confirm_success - estimate: 15s', 'yellow'))

        for i in range(3):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            deleted_hex = get_random_node_and_delete()

            browser.switch_to_alert().accept()
            sleep(2*SLEEP_INTERVAL)

            print(colored('\ttest_3_delete_confirm_success: confirm delete - asserting...', 'blue'))
            assert "The AMR Device with Hex. Address " + deleted_hex + " has been deleted successfully." in browser.page_source

            print(colored('\ttest_3_delete_confirm_success: check modal - asserting...', 'blue'))
            self.assertFalse(check_existence('//div[@class="MuiFormControl-root"]', is_id=False))

            node_table_headers = get_table_headers()
            rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
            hexes = []
            for row in rows:
                hexes.append(row.find_elements_by_tag_name('td')[node_table_headers.index('Hex. Address')].get_attribute('innerHTML'))

            print(colored('\ttest_3_delete_confirm_success: check deleted hex address - asserting...', 'blue'))
            assert deleted_hex not in hexes

        print(colored('\ttest_3_delete_confirm_success: passed.', 'cyan'))


if __name__ == '__main__':
    runNodeDeleteTest = NodeDeleteTest()
    print(colored('NodeDeleteTest - ' + str(runNodeDeleteTest.countTestCases()) + ' tests in detail modal.', 'green'))
    runNodeDeleteTest.test_1_delete_unconfirm()
    runNodeDeleteTest.test_2_delete_confirm_no_network()
    runNodeDeleteTest.test_3_delete_confirm_success()
