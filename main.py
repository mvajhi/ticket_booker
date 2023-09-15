from simple_term_menu import TerminalMenu
from ali_bot import Ali_bot

bot = Ali_bot()


def main():
    while True:
        main_menu()


def menu(options):
    op_list = list(options.keys())
    terminal_menu = TerminalMenu(op_list)
    menu_entry_index = terminal_menu.show()
    options[op_list[menu_entry_index]]()

def main_menu():
    options = {
        "login": login_menu,
        "exit": close_app
    }
    menu(options)

def login_menu():
    options = {
        "login with password": login_with_pass,
        "login with phone number": login_with_phone
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

if __name__ == "__main__":
    main()
