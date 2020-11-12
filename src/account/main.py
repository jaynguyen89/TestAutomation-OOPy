import os.path

from src.root import Root
from src.utility import browser
from src.utility import get_tests_to_run, make_test_list

if __name__ == '__main__':
    Root.navigate_to(browser, 'Administration/ManageUser')

    tests = [name for name in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "\\account")
             if "main" not in name and "__" not in name]

    test_list = make_test_list(tests)
    tests_to_run = get_tests_to_run(test_list, len(tests))

    for test in tests_to_run:
        exec(
            open(
                os.path.dirname(os.path.realpath(__file__)) + "\\account\\" + tests[test - 1]
            ).read(),
            globals(),
            locals()
        )
