from colorama import Fore
from simple_term_menu import TerminalMenu
from ali_bot import Ali_bot

bot = Ali_bot()


def main():
    while True:
        main_menu()


def print_status():
    print("\n" * 12)

    if bot.check_login():
        print(Fore.GREEN + "Login: OK")
    else:
        print(Fore.RED + "Login: NOT OK")
    
    print("\n")
        


def menu(options):
    op_list = list(options.keys())
    terminal_menu = TerminalMenu(op_list)
    menu_entry_index = terminal_menu.show()
    options[op_list[menu_entry_index]]()

def main_menu():
    print_status()
    options = {
        "login": login_menu,
        "set this page as main": set_main_page,
        "fill register": fill_register,
        "test": test,
        "exit": close_app
    }
    menu(options)

def login_menu():
    options = {
        "login with password": login_with_pass,
        "login with phone number": login_with_phone,
        "back to home": main_menu
    }
    menu(options)

# TODO check login before
def login_with_pass():
    phone = input("enter phone number: +98 ")
    password = input("enter password: ")
    bot.login_with_user_pass(phone, password)


def login_with_phone():
    phone = input("enter phone number: +98 ")
    bot.login_with_phone(phone)
    register_code = input("enter register code: ")
    bot.enter_register_code(register_code)

def close_app():
    # TODO
    exit()

def set_main_page():
    bot.set_main_page()

def fill_register():
    bot.fill_register_form({
        "first_name" : "علی",
        "last_name" : "جوادی",
        "nid" : "0150545213",
        "gender" : "male",
        "birthday" : {"day" : "18", "month" : "12", "year" : "1362"}
        })

def test():
    bot.test()


if __name__ == "__main__":
    main()
