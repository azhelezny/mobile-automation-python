from mobile_ui_entries.impl.Button import Button
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import UserPropertiesPageLocators
from config_entries.Properties import Properties

__author__ = 'andrey'


class UserPropertiesPage(BasicPage):
    @staticmethod
    def logout():
        UserPropertiesPage.return_logout_button().click()

    @staticmethod
    def return_logout_button():
        return Button(
            Properties.get_user_properties_page_locator_map().get_locator(UserPropertiesPageLocators.logoutButton))