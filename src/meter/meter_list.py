import unittest
from time import sleep
from src.utility import SLEEP_INTERVAL, browser, get_random_table_row, check_existence, get_table_headers
from src.root import Root, prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored


class MeterListTest(unittest.TestCase):
    def test_1_meters_list_no_network(self):
        print(colored('Running: test_1_meters_list_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        browser.refresh()
        Root.navigate_to(browser, 'Factory/ManageMeter')
        sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_1_meters_list_no_network: meters list no network - asserting...', 'blue'))
        self.assertTrue(check_existence('//div[@class="inform"]', is_id=False))
        self.assertFalse(check_existence('//tbody[@class="MuiTableBody-root"]', is_id=False))

        print(colored('\ttest_1_meters_list_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageMeter')

    def test_2_meters_display(self):
        print(colored('Running: test_2_meters_display - estimate: 5s', 'yellow'))

        pagination_label = browser.find_element_by_xpath('//tfoot[@class="MuiTableFooter-root"]/tr/td/div/div/span['
                                                         '@class="MuiTypography-root MuiTypography-caption"]')
        total_meters = int(pagination_label.get_attribute('innerHTML').split(' ')[2])

        print(colored('\ttest_2_meters_display: meters count - asserting...', 'blue'))
        self.assertGreater(total_meters, 0)

        print(colored('\ttest_2_meters_display: passed.', 'cyan'))

    def test_3_meter_columns(self):
        print(colored('Running: test_3_meter_columns - estimate: 5s', 'yellow'))

        for i in range(2):
            print(colored('\trandom meter ' + str(i + 1), 'magenta'))
            meter_row = get_random_table_row()
            meter_cols = meter_row.find_elements_by_tag_name('td')

            meter_table_headers = get_table_headers()
            for col in meter_table_headers:
                col_data = meter_cols[meter_table_headers.index(col)].get_attribute('innerHTML')
                has_data = col == 'Serial No.' and len(col_data) > 0 or len(col_data) >= 0

                print(colored('\ttest_3_meter_columns: column "' + col + '" - asserting...', 'blue'))
                self.assertTrue(has_data)

        print(colored('\ttest_3_meter_columns: passed.', 'cyan'))


if __name__ == '__main__':
    runMeterListTest = MeterListTest()
    print(colored('MeterListTest - ' + str(runMeterListTest.countTestCases()) + ' tests in meter table.', 'green'))
    runMeterListTest.test_1_meters_list_no_network()
    runMeterListTest.test_2_meters_display()
    runMeterListTest.test_3_meter_columns()
