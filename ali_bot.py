from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

class Ali_bot:
    # TODO use other browsers
    def __init__(self):
        self.__ali_url = "https://alibaba.ir/"
        self.__driver = webdriver.Firefox()
        self.__driver.get(self.__ali_url)
    
    # TODO
    def check_login(self):
        return False
    
    '''after use this you should call enter_register_code'''
    def login_with_phone(self, phone_num):
        if self.check_login():
            raise "login before"
        self.__open_login_page()

        mobile_field = self.__driver.find_element(By.XPATH, value= '//input[@name="mobile"]')
        accept_button = self.__driver.find_element(By.XPATH, value='//button[text()=" تایید و دریافت کد "]')
        
        mobile_field.send_keys(phone_num)
        accept_button.click()

    def __open_login_page(self):
        login_button = self.__driver.find_element(By.XPATH, value='//span[text()=" ورود یا ثبت‌نام "]')
        login_button.click()

    def enter_register_code(self, register_code):
        num_fields = self.__driver.find_elements(By.XPATH, value='//div[contains(@class, "digits justify-between text-center mb-6")]/input')
        for i in range(len(num_fields)):
            num_fields[i].send_keys(register_code[i])
    