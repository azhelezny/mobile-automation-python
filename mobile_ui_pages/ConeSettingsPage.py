__author__ = 'andrey'

import time
from general_utils import text_utils
from mobile_ui_entries.impl.InputField import InputField
from mobile_ui_entries.impl.Button import Button
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import ConeSettingsPageLocators
from config_entries.Properties import Properties


class ConeSettingsPage(BasicPage):
    @staticmethod
    def wait_for_equalizer_state(new_state, retries=10):
        for i in range(retries):
            if text_utils.smart_compare(new_state, ConeSettingsPage.get_eq_status()):
                return True
            time.sleep(1)
        return False

    @staticmethod
    def get_cone_name():
        return InputField(
            Properties.get_cone_settings_page_locator_map().get_locator(ConeSettingsPageLocators.coneName)).get_text()

    @staticmethod
    def get_eq_status():
        return InputField(
            Properties.get_cone_settings_page_locator_map().get_locator(
                ConeSettingsPageLocators.eqState)).get_text().strip()

    @staticmethod
    def equalizer_click():
        Button(Properties.get_cone_settings_page_locator_map().get_locator(
            ConeSettingsPageLocators.equalizerButton)).click()

    @staticmethod
    def set_equalizer(eq_name):
        ConeSettingsPage.equalizer_click()
        locator = Properties.get_cone_settings_page_locator_map().get_locator(ConeSettingsPageLocators.eqSet)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", eq_name)
        Button(locator).click()

    @staticmethod
    def back_click():
        Button(
            Properties.get_cone_settings_page_locator_map().get_locator(ConeSettingsPageLocators.back)).click()

    @staticmethod
    def link_click(name):
        locator = Properties.get_cone_settings_page_locator_map().get_locator(ConeSettingsPageLocators.coneNameInLan)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
        Button(locator).click()


