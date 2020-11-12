import unittest
from time import sleep
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_table_row, get_table_headers
from src.root import Root, prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored


class GatewayCmdListTest(unittest.TestCase):
    def test_1_commands_list_no_network(self):
        print(colored('Running: test_1_commands_list_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        browser.refresh()
        Root.navigate_to(browser, 'Administration/GatewayCommand')
        sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_1_commands_list_no_network: commands list no network - asserting...', 'blue'))
        self.assertTrue(check_existence('//div[@class="inform"]', is_id=False))
        self.assertFalse(check_existence('//tbody[@class="MuiTableBody-root"]', is_id=False))

        print(colored('\ttest_1_commands_list_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Administration/GatewayCommand')

    def test_2_commands_display(self):
        print(colored('Running: test_2_commands_display - estimate: 5s', 'yellow'))

        pagination_label = browser.find_element_by_xpath('//tfoot[@class="MuiTableFooter-root"]/tr/td/div/div/span['
                                                         '@class="MuiTypography-root MuiTypography-caption"]')
        total_commands = int(pagination_label.get_attribute('innerHTML').split(' ')[2])

        print(colored('\ttest_2_commands_display: commands count - asserting...', 'blue'))
        self.assertGreater(total_commands, 0)

        print(colored('\ttest_2_commands_display: passed.', 'cyan'))

    def test_3_commands_columns(self):
        print(colored('Running: test_3_commands_columns - estimate: 5s', 'yellow'))
        commands_table_headers = get_table_headers()

        for i in range(2):
            print(colored('\trandom commands ' + str(i + 1), 'magenta'))
            commands_row = get_random_table_row()
            commands_cols = commands_row.find_elements_by_tag_name('td')

            for col in commands_table_headers:
                col_data = commands_cols[commands_table_headers.index(col)].get_attribute('innerHTML')
                has_data = (col == 'Command' or col == 'Type') and len(col_data) > 0 or len(col_data) >= 0

                print(colored('\ttest_3_commands_columns: column "' + col + '" - asserting...', 'blue'))
                self.assertTrue(has_data)

        print(colored('\ttest_3_commands_columns: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewayCmdListTest = GatewayCmdListTest()
    print(colored('GatewayCmdListTest - ' + str(runGatewayCmdListTest.countTestCases()) + ' tests in node table.',
                  'green'))
    runGatewayCmdListTest.test_1_commands_list_no_network()
    runGatewayCmdListTest.test_2_commands_display()
    runGatewayCmdListTest.test_3_commands_columns()
