import unittest
import random
from time import sleep
from datetime import date
from selenium.webdriver.common.keys import Keys
from src.utility import SLEEP_INTERVAL, browser, faker, check_existence, get_random_table_row, get_table_headers
from faker.providers import lorem
from termcolor import colored

faker.add_provider(lorem)
SEARCH_FORM_IDs = ['gw-search-clear', 'gw-search-keyword', 'gw-search-date-from', 'gw-search-date-to',
                   'gw-search-inverted', 'gw-search-inactive', 'gw-search-button']


class SearchForm:
    def __init__(self):
        self.keyword_input = browser.find_element_by_id('gw-search-keyword')
        self.search_fields = browser.find_elements_by_name('gw-search-fields')
        self.date_from_input = browser.find_element_by_id('gw-search-date-from')
        self.date_to_input = browser.find_element_by_id('gw-search-date-to')
        self.inverted_input = browser.find_element_by_id('gw-search-inverted')
        self.inactive_input = browser.find_element_by_id('gw-search-inactive')
        self.form_clear_button = browser.find_element_by_id('gw-search-clear')
        self.search_button = browser.find_element_by_id('gw-search-button')

    def check_random_search_field(self):
        random_field = random.choice(self.search_fields)
        browser.execute_script('arguments[0].click()', random_field)


class GatewaySearchFormTest(unittest.TestCase):
    def test_1_search_form_elements(self):
        print(colored('Running: test_1_search_form_elements - estimate: 1s', 'yellow'))

        for element_id in SEARCH_FORM_IDs:
            print(colored('\ttest_1_search_form_elements: input "' + element_id + '" existence - asserting...', 'blue'))
            self.assertTrue(check_existence(element_id))

        search_form = SearchForm()
        print(colored('\ttest_1_search_form_elements: element status - asserting...', 'blue'))
        self.assertFalse(search_form.inverted_input.is_selected())
        self.assertFalse(search_form.inactive_input.is_selected())
        self.assertFalse(search_form.search_button.is_enabled())

        print(colored('\ttest_1_search_form_elements: passed.', 'cyan'))

    def test_2_error_handling(self):
        print(colored('Running: test_2_error_handling - estimate: 13s', 'yellow'))

        search_form = SearchForm()
        search_form.keyword_input.send_keys(faker.word())
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "At least 1 Search Field must be selected to perform search." in browser.page_source
        self.assertFalse(search_form.search_button.is_enabled())

        search_form.check_random_search_field()
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "At least 1 Search Field must be selected to perform search." not in browser.page_source
        self.assertTrue(search_form.search_button.is_enabled())

        browser.execute_script('arguments[0].click()', search_form.inverted_input)
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "No date range to invert. Please set a date range first." in browser.page_source
        self.assertFalse(search_form.inverted_input.is_selected())
        self.assertTrue(search_form.search_button.is_enabled())

        search_form.date_from_input.send_keys(date.today().strftime("%d/%m/%Y"))
        browser.execute_script('arguments[0].click()', search_form.inverted_input)
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "No date range to invert. Please set a date range first." in browser.page_source
        self.assertFalse(search_form.inverted_input.is_selected())
        self.assertTrue(search_form.search_button.is_enabled())

        search_form.date_to_input.send_keys(date.today().strftime("%d/%m/%Y"))
        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        self.assertFalse(check_existence('//div[@class="alert alert-warning"]', is_id=False))
        self.assertTrue(search_form.search_button.is_enabled())

        browser.execute_script('arguments[0].click()', search_form.inverted_input)
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "No date range to invert. Please set a date range first." in browser.page_source
        self.assertFalse(search_form.inverted_input.is_selected())
        self.assertTrue(search_form.search_button.is_enabled())

        search_form.form_clear_button.send_keys(Keys.ENTER)
        sleep(SLEEP_INTERVAL)

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        self.assertFalse(search_form.search_button.is_enabled())

        search_form.keyword_input.send_keys(faker.word())
        browser.execute_script('arguments[0].click()', search_form.search_fields[0])
        browser.execute_script('arguments[0].click()', search_form.search_fields[0])

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "At least 1 Search Field must be selected to perform search." in browser.page_source
        self.assertFalse(search_form.search_button.is_enabled())

        search_form.date_from_input.send_keys(date.today().strftime("%d/%m/%Y"))
        search_form.date_to_input.send_keys(date.today().strftime("%d/%m/%Y"))

        print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        assert "At least 1 Search Field must be selected to perform search." in browser.page_source
        self.assertFalse(search_form.search_button.is_enabled())

        # search_form.check_random_search_field()
        # search_form.date_to_input.send_keys('1-1-2000')
        #
        # print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        # assert "Date From should not be greater than Date To. Please check date range." in browser.page_source
        # self.assertFalse(search_form.search_button.is_enabled())
        #
        # search_form.date_to_input.send_keys('1-1-1999')
        #
        # print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        # assert "Date From should not be greater than Date To. Please check date range." not in browser.page_source
        # self.assertTrue(search_form.search_button.is_enabled())
        #
        # search_form.inverted_input.click()
        # search_form.date_to_input.send_keys('1-1-1999')
        #
        # print(colored('\ttest_2_error_handling: alert message - asserting...', 'blue'))
        # assert "Date From should not be greater than Date To. Please check date range." in browser.page_source
        # self.assertFalse(search_form.search_button.is_enabled())

        print(colored('\ttest_2_error_handling: passed.', 'cyan'))

    def test_3_search_success(self):
        print(colored('Running: test_3_search_success - estimate: 13s', 'yellow'))
        search_form = SearchForm()
        search_form.form_clear_button.send_keys(Keys.ENTER)
        gateway_table_headers = get_table_headers()

        keyword = ''
        for i in range(5):
            random_row = get_random_table_row()
            cols = random_row.find_elements_by_tag_name('td')
            keyword += (cols[gateway_table_headers.index('Imei')].get_attribute('innerHTML') + ",")

        keyword = keyword[:-1]

        search_form.keyword_input.send_keys(keyword)
        browser.execute_script('arguments[0].click()', search_form.search_fields[0])

        search_form.search_button.send_keys(Keys.ENTER)

        sleep(2*SLEEP_INTERVAL)
        results = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
        result_imeis = []
        for result in results:
            cols = result.find_elements_by_tag_name('td')
            if len(cols) != 0:
                result_imeis.append(cols[gateway_table_headers.index('Imei')].get_attribute('innerHTML'))

        keyword_imeis = keyword.split(',')
        print(colored('\ttest_3_search_success: matching results - asserting...', 'blue'))
        self.assertEqual(keyword_imeis.sort(), result_imeis.sort())

        print(colored('\ttest_3_search_success: passed.', 'cyan'))


if __name__ == '__main__':
    runGatewaySearchFormTest = GatewaySearchFormTest()
    print(colored(
        'GatewaySearchFormTest - ' + str(runGatewaySearchFormTest.countTestCases()) + ' tests in update gateway.',
        'green'))
    runGatewaySearchFormTest.test_1_search_form_elements()
    runGatewaySearchFormTest.test_2_error_handling()
    runGatewaySearchFormTest.test_3_search_success()
