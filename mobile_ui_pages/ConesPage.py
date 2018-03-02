import time
from mobile_ui_pages.PlayListPage import PlayListPage
from mobile_ui_entries.impl.Button import Button
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import ConesPageLocators
from config_entries.Properties import Properties

__author__ = 'andrey'


class ConesPage(BasicPage):
    @staticmethod
    def cones_settings_click(name):
        ConesPage.__swipe_from()
        if Properties.if_ios():
            ConesPage.return_settings_button().click()
            ConesPage.choose_by_name(name)
        else:
            locator = Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.coneSettings)
            locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
            settings_button = Button(locator)
            location = settings_button.get_location()
            size = settings_button.get_size()
            x = location["x"]
            y = location["y"] + size["height"] // 2
            Button(locator).click()
            ConesPage.tap_on(x, y)

    @staticmethod
    def link_cones(name1, name2):
        if Properties.if_ios():
            first_cone = ConesPage.return_cone_by_name(name1)
            second_cone = ConesPage.return_cone_by_name(name2)
            ConesPage.drag_cone_to_cone(second_cone, first_cone)
        else:
            ConesPage.link_or_unlink_cones(name1, name2)

    @staticmethod
    def unlink_cones(name1, name2):
        if Properties.if_ios():
            ConesPage.__swipe_from()
            second_cone = ConesPage.return_cone_by_name(name2)
            ConesPage.long_press_on_element(second_cone)
        else:
            ConesPage.link_or_unlink_cones(name1, name2)

    @staticmethod
    def link_or_unlink_cones(name1, name2):
        ConesPage.cones_settings_popup(name1)
        ConesPage.return_link_to_cone().click()
        ConesPage.return_radio_cone(name2).click()
        ConesPage.return_pop_up_ok().click()

    @staticmethod
    def unlink_cones_by_unlink_group(name):
        ConesPage.cones_settings_popup(name)
        ConesPage.return_unlink_group().click()

    @staticmethod
    def unlink_cones_by_unlink_cone(name):
        ConesPage.cones_settings_popup(name)
        ConesPage.return_unlink_cone().click()

    @staticmethod
    def choose_by_name(name):
        ConesPage.__swipe_from()
        ConesPage.return_cone_by_name(name).click()

    @staticmethod
    def drag_cone_to_cone(from_cone, to_cone):
        ConesPage.__swipe_from()
        ConesPage._move_element_to_element(from_cone, to_cone)

    @staticmethod
    def __swipe_from():
        if PlayListPage.return_play_pause_button().is_presented(15):
            if Properties.if_ios():
                if ConesPage.return_settings_button().is_visible(3):
                    locator = ConesPage.return_settings_button()
                else:
                    locator = ConesPage.return_done_button()
            else:
                locator = ConesPage.return_user_name_button()
            if locator.is_visible(5):
                # Cones page can disappear
                time.sleep(3)
                if locator.is_visible(3):
                    return
                ConesPage.swipe_right()
                time.sleep(3)
            else:
                ConesPage.swipe_right()
                time.sleep(3)
        else:
            raise RuntimeError("Right SWIPE problem - unable to find  play/pause button")

    @staticmethod
    def return_cone_by_name(name):
        locator = Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.cone)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
        return Button(locator)

    @staticmethod
    def return_user_name_button():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.userName))

    @staticmethod
    def return_settings_button():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.coneSettings))

    @staticmethod
    def return_done_button():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.done))

    @staticmethod
    def cones_settings_popup(name):
        ConesPage.__swipe_from()
        locator = Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.coneSettings)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
        Button(locator).click()

    @staticmethod
    def return_link_to_cone():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.linkToCone))

    @staticmethod
    def return_radio_cone(name):
        locator = Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.coneOnPopup)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
        return Button(locator)

    @staticmethod
    def return_pop_up_ok():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.popUpOK))

    @staticmethod
    def return_unlink_group():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.unlinkGroup))

    @staticmethod
    def return_unlink_cone():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.unlinkCone))

    @staticmethod
    def is_master():
        return Button(Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.masterCone)).is_presented()

    @staticmethod
    def is_slave():
        return Button(
            Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.slaveLastCone)).is_presented()

    @staticmethod
    def done_click():
        Button(
            Properties.get_cones_page_locator_map().get_locator(ConesPageLocators.done)).click()