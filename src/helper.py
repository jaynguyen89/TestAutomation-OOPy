import random
from time import sleep
from src.utility import SLEEP_INTERVAL, browser, get_random_table_row, get_table_headers, click_action_button, click_delete_button


# Helpers for Authentication Tests
def assert_checking(self, statement):
    sleep(10*SLEEP_INTERVAL)
    assert statement in browser.page_source

    error_message = browser.find_element_by_class_name('alert')
    assert "alert-danger" in error_message.get_attribute('class')

    sleep(21*SLEEP_INTERVAL)
    self.assertEqual(error_message.is_displayed(), False)


# End helpers for Authentication Tests

# Helpers for Meter Tests
def get_random_meter():
    meter_row = get_random_table_row()
    meter_cols = meter_row.find_elements_by_tag_name('td')

    meter_table_headers = get_table_headers()
    meter_serial = meter_cols[meter_table_headers.index('Serial No.')].get_attribute('innerHTML')
    click_action_button(meter_cols)

    return meter_serial


def get_back_previously_updated_meter(serial):
    meter_table_headers = get_table_headers()
    rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        if serial == cols[meter_table_headers.index('Serial No.')].get_attribute('innerHTML'):
            click_action_button(cols)
            break


def get_random_meter_and_delete():
    meter_row = get_random_table_row()
    meter_cols = meter_row.find_elements_by_tag_name('td')

    meter_table_headers = get_table_headers()
    deleted_serial = meter_cols[meter_table_headers.index('Serial No.')].get_attribute('innerHTML')
    click_action_button(meter_cols)
    click_delete_button()

    return deleted_serial


# End helpers for Meter Tests

# Helpers for Device Tests
def get_random_node():
    node_row = get_random_table_row()
    node_cols = node_row.find_elements_by_tag_name('td')

    node_table_headers = get_table_headers()
    node_hex = node_cols[node_table_headers.index('Hex. Address')].get_attribute('innerHTML')
    click_action_button(node_cols)

    return node_hex


def get_back_previously_updated_node(hex):
    node_table_headers = get_table_headers()
    rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        if hex == cols[node_table_headers.index('Hex. Address')].get_attribute('innerHTML'):
            click_action_button(cols)
            break


def get_random_node_and_delete():
    node_row = get_random_table_row()
    node_cols = node_row.find_elements_by_tag_name('td')

    node_table_headers = get_table_headers()
    deleted_hex = node_cols[node_table_headers.index('Hex. Address')].get_attribute('innerHTML')
    click_action_button(node_cols)
    click_delete_button()

    return deleted_hex


# End helpers for Device Tests

# Helpers for GatewayCommand Tests
def get_random_command():
    while True:
        command_row = get_random_table_row()
        command_cols = command_row.find_elements_by_tag_name('td')

        if len(command_cols) > 0:
            break

    command_table_headers = get_table_headers()
    command = command_cols[command_table_headers.index('Command')].get_attribute('innerHTML')
    click_action_button(command_cols)

    return command


def get_back_previously_updated_command(cmd):
    command_table_headers = get_table_headers()
    rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        if len(cols) > 0 and cmd == cols[command_table_headers.index('Command')].get_attribute('innerHTML'):
            click_action_button(cols)
            break


def get_random_command_and_delete():
    while True:
        command_row = get_random_table_row()
        command_cols = command_row.find_elements_by_tag_name('td')

        if len(command_cols) > 0:
            break

    command_table_headers = get_table_headers()
    deleted_cmd = command_cols[command_table_headers.index('Name')].get_attribute('innerHTML')
    click_action_button(command_cols)
    click_delete_button()

    return deleted_cmd


# End helpers for GatewayCommand Tests

# End helpers for Gateway Tests
def get_random_gateway():
    gateway_row = get_random_table_row()
    gateway_cols = gateway_row.find_elements_by_tag_name('td')

    gateway_table_headers = get_table_headers()
    gateway_imei = gateway_cols[gateway_table_headers.index('Imei')].get_attribute('innerHTML')
    click_action_button(gateway_cols)

    return gateway_imei


def get_back_previously_updated_gateway(imei):
    gateway_table_headers = get_table_headers()
    rows = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]/tr')
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        if imei == cols[gateway_table_headers.index('Imei')].get_attribute('innerHTML'):
            click_action_button(cols)
            break


# End helpers for Gateway Tests

# End helpers for Account Tests
def get_random_row_in_account_table(active=True):
    user_tables = browser.find_elements_by_xpath('//tbody[@class="MuiTableBody-root"]')
    rows = user_tables[0].find_elements_by_tag_name('tr')

    if not active:
        rows = user_tables[1].find_elements_by_tag_name('tr')

    users = [row for row in rows if len(row.find_elements_by_tag_name('td')) > 0]
    return random.choice(users)


def get_random_account_data(account_list):
    rows = account_list.find_elements_by_tag_name('tr')
    rows = [row for row in rows if len(row.find_elements_by_tag_name('td')) > 0]

    random_row = random.choice(rows)
    return random_row.find_elements_by_tag_name('td')


# End helpers for Account Tests
