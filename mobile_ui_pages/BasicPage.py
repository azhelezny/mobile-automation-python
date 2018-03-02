from mobile_ui_entries.basics.BasicUiEntry import BasicUiEntry

__author__ = 'andrey'

from mobile_ui_searcher.Searcher import Searcher


class PrimDirection:
    up = 0
    down = 1


class BasicPage(object):
    @staticmethod
    def is_alert_present():
        return Searcher.is_alert_present()

    @staticmethod
    def get_alert_text():
        return Searcher.get_alert_text()

    @staticmethod
    def alert_accept():
        Searcher.alert_accept()

    @staticmethod
    def alert_decline():
        Searcher.alert_decline()

    @staticmethod
    def swipe_up(swipe_percent=50):
        return Searcher.swipe_up(swipe_percent)

    @staticmethod
    def swipe_down(swipe_percent=50):
        return Searcher.swipe_down(swipe_percent)

    @staticmethod
    def swipe_up_to_element(element, swipe_percent=50, timeout=1, prim_timeout=0):
        return Searcher.swipe_up_to_element(element.locator, swipe_percent, timeout, prim_timeout)

    @staticmethod
    def swipe_up_from_element(element, swipe_percent=50, timeout=1, prim_timeout=0):
        return Searcher.swipe_up_from_element(element.locator, swipe_percent, timeout, prim_timeout)

    @staticmethod
    def swipe_down_to_element(element, swipe_percent=50, timeout=1, prim_timeout=0):
        return Searcher.swipe_down_to_element(element.locator, swipe_percent, timeout, prim_timeout)

    @staticmethod
    def swipe_down_from_element(element, swipe_percent=50, timeout=1, prim_timeout=0):
        return Searcher.swipe_down_from_element(element.locator, swipe_percent, timeout, prim_timeout)

    @staticmethod
    def swipe_right():
        Searcher.swipe_right()

    @staticmethod
    def swipe_left():
        Searcher.swipe_left()

    @staticmethod
    def click_search_button_on_keyboard():
        Searcher.click_search_button()

    @staticmethod
    def tap_on_screen_center():
        Searcher.tap_on_screen_center()

    @staticmethod
    def tap_on(x, y):
        Searcher.tap_on(x, y)

    @staticmethod
    def _move_element_to_element(from_element, to_element, time_to_hold=3):
        Searcher.long_press_to_element_and_move_to_other_element(from_element.get_element(), to_element.get_element(),
                                                                 time_to_hold)
    @staticmethod
    def long_press_on_element(element, time_to_hold=3):
        Searcher.long_press_on_element(element.get_element(), time_to_hold)

    @staticmethod
    def put_app_in_background(time_idle):
        Searcher.put_app_in_background(time_idle)

    @staticmethod
    def _increase_volume_by_application_button(taps_quantity):
        for i in range(taps_quantity):
            Searcher.increase_volume_by_application_button()

    @staticmethod
    def _decrease_volume_by_application_button(taps_quantity):
        for i in range(taps_quantity):
            Searcher.decrease_volume_by_application_button()

    @staticmethod
    def increase_volume_by_device_button(taps_quantity):
        for i in range(taps_quantity):
            Searcher.increase_volume_by_device_button()

    @staticmethod
    def decrease_volume_by_device_button(taps_quantity):
        for i in range(taps_quantity):
            Searcher.decrease_volume_by_device_button()

    @staticmethod
    def back():
        Searcher.back()