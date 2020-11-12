import unittest
from time import sleep
from src.utility import SLEEP_INTERVAL, browser, get_random_table_row, check_existence, get_table_headers
from src.root import Root, prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored


class GatewayListTest(unittest.TestCase):
    def test_1_gateways_list_no_network(self):
        print(colored('Running: test_1_gateways_list_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        browser.refresh()
        Root.navigate_to(browser, 'Factory/ManageGateways')
        sleep(9+SLEEP_INTERVAL)

        print(colored('\ttest_1_gateways_list_no_network: gateways list no network - asserting...', 'blue'))
        self.assertTrue(check_existence('//div[@class="inform"]', is_id=False))
        self.assertFalse(check_existence('//tbody[@class="MuiTableBody-root"]', is_id=False))
        self.assertFalse(check_existence('gateway-search-form'))

        print(colored('\ttest_1_gateways_list_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageGateways')

    def test_2_gateways_display(self):
        print(colored('Running: test_2_gateways_display - estimate: 5s', 'yellow'))

        pagination_label = browser.find_element_by_xpath('//tfoot[@class="MuiTableFooter-root"]/tr/td/div/div/span['
                                                         '@class="MuiTypography-root MuiTypography-caption"]')
        total_gateways = int(pagination_label.get_attribute('innerHTML').split(' ')[2])

        print(colored('\ttest_2_gateways_display: gateways count - asserting...', 'blue'))
        self.assertGreater(total_gateways, 0)

        print(colored('\ttest_2_gateways_display: passed.', 'cyan'))

    def test_3_gateway_columns(self):
        print(colored('Running: test_3_gateway_columns - estimate: 5s', 'yellow'))
        gateway_table_headers = get_table_headers()

        for i in range(2):
            print(colored('\trandom gateway ' + str(i + 1), 'magenta'))
            gateway_row = get_random_table_row()
            gateway_cols = gateway_row.find_elements_by_tag_name('td')

            for col in gateway_table_headers:
                col_data = gateway_cols[gateway_table_headers.index(col)].get_attribute('innerHTML')
                has_data = col == 'Imei' and len(col_data) > 0 or len(col_data) >= 0

                print(colored('\ttest_3_gateway_columns: column "' + col + '" - asserting...', 'blue'))
                self.assertTrue(has_data)

        print(colored('\ttest_3_gateway_columns: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayListTest = GatewayListTest()
    print(
        colored('GatewayListTest - ' + str(runGatewayListTest.countTestCases()) + ' tests in gateway table.', 'green'))
    runGatewayListTest.test_1_gateways_list_no_network()
    runGatewayListTest.test_2_gateways_display()
    runGatewayListTest.test_3_gateway_columns()
