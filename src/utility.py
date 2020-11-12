import random
import re
from pathlib import Path
from time import sleep

from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from termcolor import colored

# Alter the below 3 global values according to your test environment
TEST_URL = "http://localhost:3000/"
LOGIN_CREDENTIALS = {'username': "JayNG", 'password': "password"}

# seconds, adjust if server response takes long to process
SLEEP_INTERVAL = 2

ROOT_DIR = Path(__file__).parent.parent
browser = webdriver.Chrome(str(ROOT_DIR) + '\\chromedriver.exe')

faker = Faker()


def make_test_list(tests):
    str_list = '\t'
    for test in tests:
        str_list += (str(tests.index(test) + 1) + ". " + test.split('.')[0] + "\n\t")

    return str_list


def get_components_to_test(comp_list, comp_quantity):
    prompt_message = "Please select the components you want to test:\n" + \
                     "\t" + colored('**Component number separated by comma, no whitespace**', 'yellow') + \
                     "\n" + comp_list + "\n\tYour selection(s): "

    while True:
        inputs = input(prompt_message)

        if len(inputs) == 0:
            print(colored('No selection was made.\n\n', 'red'))
        elif re.search(r'[-]?[\d,]+$', inputs) is None:
            print(colored('Invalid format: Component number separated by comma, no whitespace\n\n', 'red'))
        else:
            comps_input = list(set(re.findall(r'([-]?\d+)', inputs)))
            comps_to_test = [int(i) for i in comps_input if comp_quantity >= int(i) > 0]

            if len(comps_to_test) == 0:
                print(colored('Component not found from your input.\n\n', 'red'))
                continue

            print(colored('\n\tComponents ' + str(comps_to_test) + ' found.\n', 'blue'))
            sleep(2*SLEEP_INTERVAL)
            return comps_to_test


def get_tests_to_run(test_list, tests_quantity):
    prompt_message = "Please select the tests you want to run:\n" + \
                     "\t" + colored('**Test number separated by comma, no whitespace**', 'yellow') + \
                     "\n" + test_list + "\n\n\tYour selection(s): "

    while True:
        inputs = input(prompt_message)

        if len(inputs) == 0:
            print(colored('No selection was made.\n\n', 'red'))
        elif re.search(r'[-]?[\d,]+$', inputs) is None:
            print(colored('Invalid format: Test number separated by comma, no whitespace\n\n', 'red'))
        else:
            tests_input = list(set(re.findall(r'([-]?\d+)', inputs)))
            tests_to_run = [int(i) for i in tests_input if tests_quantity >= int(i) > 0]

            if len(tests_to_run) == 0:
                print(colored('Found no test from your input.\n\n', 'red'))
                continue

            print(colored('\n\tTests number ' + str(tests_to_run) + ' found. Now running...\n\n', 'blue'))
            sleep(2*SLEEP_INTERVAL)
            return tests_to_run


def check_existence(selector, by='xpath', multiple=False, is_id=True):
    try:
        if is_id:
            if selector != 'login_btn':
                browser.find_element_by_id(selector)
            else:
                browser.find_element_by_css_selector("button[type='submit']")
        elif multiple:
            if by == 'xpath':
                browser.find_elements_by_xpath(selector)
        else:
            if by == 'xpath':
                browser.find_element_by_xpath(selector)
    except NoSuchElementException:
        return False

    return True


def trigger_navbar():
    sleep(SLEEP_INTERVAL)
    browser.find_element_by_id('site-icon-nav-trigger').click()
    sleep(SLEEP_INTERVAL)


def logout():
    browser.find_element_by_id('avatar-link').click()
    browser.find_element_by_id('user-card-header').click()

    sleep(2*SLEEP_INTERVAL)
    logout_btn = browser.find_element_by_id('logout-item')
    logout_btn.click()


def clear_inputs(selectors, by):
    for selector in selectors:
        if by == 'id':
            browser.find_element_by_id(selector).send_keys(Keys.CONTROL + 'a')
            browser.find_element_by_id(selector).send_keys(Keys.DELETE)


def click_fab_button():
    fab_button = browser.find_element_by_id('juice-fab').find_element_by_tag_name('button')
    fab_button.send_keys(Keys.ENTER)
    sleep(3+SLEEP_INTERVAL)


def click_save_button():
    save_button = browser.find_element_by_id('save-button')
    save_button.send_keys(Keys.ENTER)
    sleep(3+SLEEP_INTERVAL)


def click_update_button():
    update_button = browser.find_element_by_id('update-button')
    update_button.send_keys(Keys.ENTER)
    sleep(3+SLEEP_INTERVAL)


def click_delete_button():
    delete_button = browser.find_element_by_id('delete-button')
    delete_button.send_keys(Keys.ENTER)
    sleep(3+SLEEP_INTERVAL)


def close_modal():
    cancel_button = browser.find_element_by_id('cancel-button')
    cancel_button.send_keys(Keys.ENTER)
    sleep(SLEEP_INTERVAL)


def click_action_button(cols):
    action_button = cols[len(cols) - 1].find_element_by_tag_name('button')
    action_button.send_keys(Keys.ENTER)
    sleep(2*SLEEP_INTERVAL)


def get_table_headers():
    header_cols = browser.find_elements_by_xpath('//span[@class="MuiButtonBase-root MuiTableSortLabel-root"]')

    headers = []
    for col in header_cols:
        headers.append(col.find_element_by_tag_name('div').get_attribute('innerHTML'))

    return remove_duplicate_preserve_order(headers)


def remove_duplicate_preserve_order(sequence):
    seen = set()
    seen_add = seen.add
    return [x for x in sequence if not (x in seen or seen_add(x))]


def get_random_table_row() -> WebElement:
    rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
    random_row = random.choice(rows)

    return random_row


def get_random_dropdown_item(items) -> WebElement:
    return random.choice(items)


def get_random_table_data(col):
    row = get_random_table_row()
    table_headers = get_table_headers()
    cols = row.find_elements_by_tag_name('td')
    col_data = cols[table_headers.index(col)].get_attribute('innerHTML')
    return col_data


def pick_random_dropdown_item(dropdown_id):
    form = browser.find_element_by_xpath('//div[@class="MuiFormControl-root"]')
    dropdown = form.find_element_by_id(dropdown_id)
    dropdown.send_keys(Keys.ENTER)
    sleep(SLEEP_INTERVAL)

    items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                           'MuiList-padding"]/div')
    if len(items) == 0:
        items = browser.find_elements_by_xpath('//ul[@class="MuiList-root MuiMenu-list '
                                               'MuiList-padding"]/li')

    random_item = get_random_dropdown_item(items)

    try:
        item_value = random_item.find_element_by_xpath('//span/div/div').get_attribute('innerHTML')
    except NoSuchElementException:
        item_value = random_item.get_attribute('innerHTML')

    random_item.click()
    sleep(SLEEP_INTERVAL)

    return item_value


def check_form_buttons(self):
    print(colored('\tcheck_form_buttons: cancel-button always exists - asserting...', 'blue'))
    self.assertTrue(check_existence('cancel-button'))

    save_btn_existed = check_existence('save-button')
    if save_btn_existed:
        print(colored('\tcheck_form_buttons: save-button exists - asserting...', 'blue'))
        self.assertFalse(check_existence('delete-button'))
        self.assertFalse(check_existence('update-button'))
    else:
        print(colored('\tcheck_form_buttons: save-button in-exists - asserting...', 'blue'))
        self.assertTrue(check_existence('delete-button'))
        self.assertTrue(check_existence('update-button'))
