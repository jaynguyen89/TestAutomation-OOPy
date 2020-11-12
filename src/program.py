import os.path
from datetime import date, datetime
from src.root import *
from src.utility import *
from src.helper import *


def make_component_list(components):
    str_list = "\t"
    for component in components:
        str_list += (str(components.index(component) + 1) + ". " + component + "\n\t")

    return str_list


class Program:
    Root.open_juice_app_on_chrome(browser)
    Root.login_user(browser, {'username': LOGIN_CREDENTIALS['username'], 'password': LOGIN_CREDENTIALS['password']})

    components = [name for name in os.listdir('.') if os.path.isdir(name)
                  and "__" not in name and "authentication" not in name]
    components_list = make_component_list(components)

    components_to_test = get_components_to_test(components_list, len(components))

    for component in components_to_test:
        component_name = components[component - 1]
        exec(open(str(ROOT_DIR) + "/src/" + component_name.lower() + "/main.py").read(), globals(), locals())

    Root.tear_down_on_test_done(browser)
