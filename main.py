from ali_bot import Ali_bot

phone = "9023874867"
password = "mahdi1234"

bot = Ali_bot()
bot.login_with_phone(phone)
register_code = input("enter register code: ")
bot.enter_register_code(register_code)
