from ali_bot import Ali_bot

bot = Ali_bot()

def main():
    login_with_phone()


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

if __name__ == "__main__":
    main()
