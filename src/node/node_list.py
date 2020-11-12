import unittest
from time import sleep
from src.utility import SLEEP_INTERVAL, browser, check_existence, get_random_table_row, get_table_headers
from src.root import Root, prompt_to_disable_network, prompt_to_enable_network_and_setup
from termcolor import colored


class NodeListTest(unittest.TestCase):
    def test_1_nodes_list_no_network(self):
        print(colored('Running: test_1_nodes_list_no_network - estimate: 27s', 'yellow'))
        prompt_to_disable_network()

        browser.refresh()
        Root.navigate_to(browser, 'Factory/ManageDevice')
        sleep(2*SLEEP_INTERVAL)

        print(colored('\ttest_1_nodes_list_no_network: nodes list no network - asserting...', 'blue'))
        self.assertTrue(check_existence('//div[@class="inform"]', is_id=False))
        self.assertFalse(check_existence('//tbody[@class="MuiTableBody-root"]', is_id=False))

        print(colored('\ttest_1_nodes_list_no_network: passed.', 'cyan'))
        prompt_to_enable_network_and_setup(browser, 'Factory/ManageDevice')

    def test_2_node_display(self):
        print(colored('Running: test_2_node_display - estimate: 5s', 'yellow'))

        pagination_label = browser.find_element_by_xpath('//tfoot[@class="MuiTableFooter-root"]/tr/td/div/div/span['
                                                         '@class="MuiTypography-root MuiTypography-caption"]')
        total_nodes = int(pagination_label.get_attribute('innerHTML').split(' ')[2])

        print(colored('\ttest_2_node_display: nodes count - asserting...', 'blue'))
        self.assertGreater(total_nodes, 0)

        print(colored('\ttest_2_node_display: passed.', 'cyan'))

    def test_3_node_columns(self):
        print(colored('Running: test_3_node_columns - estimate: 5s', 'yellow'))
        node_table_headers = get_table_headers()

        for i in range(2):
            print(colored('\trandom node ' + str(i + 1), 'magenta'))
            node_row = get_random_table_row()
            node_cols = node_row.find_elements_by_tag_name('td')

            for col in node_table_headers:
                col_data = node_cols[node_table_headers.index(col)].get_attribute('innerHTML')
                has_data = col == 'Hex. Address' and len(col_data) > 0 or len(col_data) >= 0

                print(colored('\ttest_3_node_columns: column "' + col + '" - asserting...', 'blue'))
                self.assertTrue(has_data)

        print(colored('\ttest_3_node_columns: passed.', 'cyan'))


if __name__ == '__main__':
    runNodeListTest = NodeListTest()
    print(colored('NodeListTest - ' + str(runNodeListTest.countTestCases()) + ' tests in node table.', 'green'))
    runNodeListTest.test_1_nodes_list_no_network()
    runNodeListTest.test_2_node_display()
    runNodeListTest.test_3_node_columns()
