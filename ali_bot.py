from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


class Element_finder:
    def __init__(self, _driver: webdriver.Firefox):
        self.__driver = _driver
        self.__fields = {
            "gender": {"male": "مرد", "female": "زن"},
            "day": {str(i): str(i) for i in range(1, 32)},
            "month": {
                "1": "فروردین",
                "2": "اردیبهشت",
                "3": "خرداد",
                "4": "تیر",
                "5": "مرداد",
                "6": "شهریور",
                "7": "مهر",
                "8": "آبان",
                "9": "آذر",
                "10": "دی",
                "11": "بهمن",
                "12": "اسفند"
            },
            "year": {str(i): str(i) for i in range(1300, 1400)}
        }

    def get_login_button(self):
        '''if dont have it return none'''
        login_button = self.__driver.find_elements(
            By.XPATH, value='//span[text()=" ورود یا ثبت‌نام "]')
        if len(login_button) == 0:
            return None
        else:
            return login_button[0]

    def get_mobile_field(self):
        return self.__driver.find_element(By.XPATH, value='//input[@name="mobile"]')

    def get_mobile_accept_button(self):
        return self.__driver.find_element(By.XPATH, value='//button[text()=" تایید و دریافت کد "]')

    def get_register_code_fields(self):
        return self.__driver.find_elements(
            By.XPATH, value='//div[contains(@class, "digits justify-between text-center mb-6")]/input')

    def get_user_pass_elements(self):
        '''return dict of web elements with keys {user, password, button}'''
        elements = dict()
        elements["user"] = self.__driver.find_element(
            By.XPATH, value='//div[contains(@class, "a-input mb-5 is-lg")]//input')
        elements["password"] = self.__driver.find_element(
            By.XPATH, value='//div[contains(@class, "a-input password-input mb-6 has-prepend is-lg")]//input')
        elements["button"] = self.__driver.find_element(
            By.XPATH, value='//button[text()=" ورود به علی‌بابا "]')
        return elements

    def login_with_pass_button(self):
        return self.__driver.find_element(By.XPATH, value='//button[text()=" ورود با کلمه عبور "]')

    def get_add_button(self):
        return self.__driver.find_element(By.XPATH, value='//span[contains(.,"اضافه کردن مسافر جدید")]')

    def get_register_inputs(self):
        '''return lists of dicts
        example:
            [{'first_name': element,
            'last_name': element,
            'nid': element,
            'gender': element,
            'birthday': {'day': elem, 'month': elem, 'year': elem}},
            {...},...]
        '''
        elements = dict()
        elements["first_name"] = self.__driver.find_elements(
            By.XPATH, value='//input[@name="namePersian"]')
        elements["last_name"] = self.__driver.find_elements(
            By.XPATH, value='//input[@name="lastNamePersian"]')
        elements["nid"] = self.__driver.find_elements(
            By.XPATH, value='//input[@name="nationalCode"]')
        elements["gender"] = self.__driver.find_elements(
            By.XPATH, value='//label[text()="جنسیت"]')
        elements["birthday"] = {
            "day": self.__driver.find_elements(
                By.XPATH, value='//label[text()="روز"]'),
            "month": self.__driver.find_elements(
                By.XPATH, value='//label[text()="ماه"]'),
            "year": self.__driver.find_elements(
                By.XPATH, value='//label[text()="سال"]')
        }

        output = [
            {
                **{j: elements[j][i]
                   for j in elements.keys() if j != "birthday"},

                "birthday": {j: elements["birthday"][j][i]
                             for j in elements["birthday"].keys()}
            }
            for i in range(len(elements["nid"]))
        ]
        return output

    def get_button(self, filed_type, filed_chosen: str):
        '''
        gender is male or female
        if not find return none
        '''
        return self.__select_span_with_content(self.__fields[filed_type][filed_chosen])

    def __select_span_with_content(self, text):
        button = self.__driver.find_elements(
            By.XPATH, f'//span[contains(.,"{text}")]')
        if len(button) == 1:
            return button[0]
        else:
            return None


class Ali_bot:
    def __init__(self):
        # TODO use other browsers
        self.__ali_url = "https://alibaba.ir/"
        self.__driver = webdriver.Firefox()
        self.__driver.get(self.__ali_url)
        self.__finder = Element_finder(self.__driver)
        self.__is_try_to_login = False

    def check_login(self):
        if self.__finder.get_login_button() == None:
            return True
        elif self.__is_try_to_login:
            self.__is_try_to_login = False
            return True
        elif self.__driver.find_element(By.XPATH, value='//button[contains(@aria-label, "ناحیه کاربری")]'):
            return False
        else:
            return True

    def login_with_phone(self, phone_num):
        '''after use this you should call enter_register_code'''
        self.__open_login_page()

        # find elements
        mobile_field = self.__finder.get_mobile_field()
        accept_button = self.__finder.get_mobile_accept_button()

        mobile_field.send_keys(phone_num)
        accept_button.click()

    def __open_login_page(self):
        self.__is_try_to_login = True
        self.__finder.get_login_button().click()

    def enter_register_code(self, register_code):
        num_fields = self.__finder.get_register_code_fields()
        for i in range(len(num_fields)):
            num_fields[i].send_keys(register_code[i])

    def login_with_user_pass(self, user, password):
        '''go to user pass page'''
        self.__open_login_page()
        self.__finder.login_with_pass_button().click()

        login_form = self.__finder.get_user_pass_elements()
        login_form["user"].send_keys(user)
        login_form["password"].send_keys(password)
        login_form["button"].click()

    def set_main_page(self):
        '''save current page as main page'''
        self.main_page = self.__driver.current_url

    def start_to_work(self):
        pass

    def fill_register_form(self, data: dict):
        fields = self.__finder.get_register_inputs()[0]
        for i in data.keys():
            if not i in {"birthday", "gender"}:
                fields[i].send_keys(data[i])
            elif i == "gender":
                self.__set_gender(fields[i], data[i])
            elif i == "birthday":
                self.__set_birthday(fields[i], data[i])

    def __set_list_field_item(self, field_name: str, field, value: str):
        field.click()
        while (button := self.__finder.get_button(field_name, value)) == None:
            pass
        button.click()

    def __set_gender(self, field, gender: str):
        '''gender is "male" or "female"'''
        self.__set_list_field_item("gender", field, gender)

    def __set_birthday(self, fields: dict, birthday: dict):
        for i in {"day", "month", "year"}:
            self.__set_list_field_item(i, fields[i], birthday[i])

    def add_register_box(self, count: int):
        for i in range(count):
            self.__finder.get_add_button().click()

    def test(self):
        pass

    def __del__(self):
        self.__driver.close()
