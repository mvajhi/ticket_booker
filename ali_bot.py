from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

class Element_finder:
    def __init__(self, _driver : webdriver.Firefox):
        self.__driver = _driver
    
    def get_login_button(self):
        '''if dont have it return none'''
        login_button = self.__driver.find_elements(By.XPATH, value='//span[text()=" ورود یا ثبت‌نام "]')
        if len(login_button) == 0:
            return None
        else:
            return login_button[0]
    
    def get_mobile_field(self):
        return self.__driver.find_element(By.XPATH, value= '//input[@name="mobile"]')
    
    def get_mobile_accept_button(self):
        return self.__driver.find_element(By.XPATH, value='//button[text()=" تایید و دریافت کد "]')
    
    def get_register_code_fields(self):
        return self.__driver.find_elements(By.XPATH, value='//div[contains(@class, "digits justify-between text-center mb-6")]/input')
    
    def get_user_pass_elements(self):
        '''return dict of web elements with keys {user, password, button}'''
        elements = dict()
        elements["user"] = self.__driver.find_element(By.XPATH, value='//div[contains(@class, "a-input mb-5 is-lg")]//input')
        elements["password"] = self.__driver.find_element(By.XPATH, value='//div[contains(@class, "a-input password-input mb-6 has-prepend is-lg")]//input')
        elements["button"] = self.__driver.find_element(By.XPATH, value='//button[text()=" ورود به علی‌بابا "]')
        return elements
    
    def login_with_pass_button(self):
        return self.__driver.find_element(By.XPATH, value='//button[text()=" ورود با کلمه عبور "]')


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
    
    def __del__(self):
        self.__driver.close()