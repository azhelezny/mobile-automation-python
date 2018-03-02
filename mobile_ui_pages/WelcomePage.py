__author__ = 'andrey'

from mobile_ui_entries.impl.InputField import InputField
from mobile_ui_entries.impl.Button import Button
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import WelcomePageLocators
from config_entries.Properties import Properties


class WelcomePage(BasicPage):

    @staticmethod
    def get_welcome_message():
        return WelcomePage.return_welcome_field().get_text()

    @staticmethod
    def get_first_page_message():
        return InputField(Properties.get_welcome_page_locator_map().get_locator(WelcomePageLocators.helpPage1Text)).get_text()

    @staticmethod
    def skip_help():
        Button(Properties.get_welcome_page_locator_map().get_locator(WelcomePageLocators.skipButton)).click()

    @staticmethod
    def return_welcome_field():
        return InputField(Properties.get_welcome_page_locator_map().get_locator(WelcomePageLocators.welcomeMessage))