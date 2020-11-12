from src.root import Root
from src.utility import browser
from src.authentication.login_form_ui import LoginForm, LoginFormUITest
from src.authentication.auth_process import AuthProcessTest
from termcolor import colored

if __name__ == '__main__':
    Root.open_juice_app_on_chrome(browser)

    runLoginFormUITest = LoginFormUITest()

    print(colored('LoginFormUITest - 3 tests in login page.', 'green'))
    runLoginFormUITest.test_1_fields_availability()

    login_form = LoginForm()
    runLoginFormUITest.test_2_missing_inputs(login_form)
    runLoginFormUITest.test_3_incorrect_credentials(login_form)

    runAuthProcessTest = AuthProcessTest()

    print(colored('AuthProcessTest - 3 tests for authentication.', 'green'))
    runAuthProcessTest.test_1_correct_credentials()
    runAuthProcessTest.test_2_session_data()
    runAuthProcessTest.test_3_logout()

    Root.tear_down_on_test_done(browser)
