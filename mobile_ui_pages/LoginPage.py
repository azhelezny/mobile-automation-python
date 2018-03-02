__author__ = 'andrey'

from mobile_ui_entries.impl.InputField import InputField
from mobile_ui_entries.impl.Button import Button
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import LoginPageLocators
from config_entries.Properties import Properties


class LoginPage(BasicPage):

    @staticmethod
    def login(login, password):
        LoginPage.get_login_field().send_keys(login)
        LoginPage.get_password_field().send_keys(password)
        LoginPage.get_login_button().click()

    @staticmethod
    def get_login_field():
        return InputField(Properties.get_login_page_locator_map().get_locator(LoginPageLocators.loginTextField))

    @staticmethod
    def get_password_field():
        return InputField(Properties.get_login_page_locator_map().get_locator(LoginPageLocators.passwordTextField))

    @staticmethod
    def get_login_button():
        return Button(Properties.get_login_page_locator_map().get_locator(LoginPageLocators.loginButton))