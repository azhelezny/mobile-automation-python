import time

__author__ = 'andrey'

from mobile_ui_searcher.CustomDriver import CustomDriver
from selenium.webdriver.common.by import By
from config_entries.Properties import Properties


class Searcher:
    driver = None
    SWIPE_VERTICAL_X = 200
    SWIPE_VERTICAL_Y = 400
    SWIPE_HORIZONTAL_X = 200
    SWIPE_HORIZONTAL_Y = 400
    SWIPE_HORIZONTAL_MOVE = 300

    SCREEN_SIZE = {}
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0

    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_VOLUME_MUTE = 164

    @staticmethod
    def get_driver():
        """:rtype : mobile_ui_searcher.CustomDriver.CustomDriver"""
        if Searcher.driver is None:
            Searcher.set_up(Properties.get_desired_capabilities())
        return Searcher.driver

    @staticmethod
    def is_element_presented(locator, wait_seconds=10):
        return Searcher.get_driver().is_element_presented(locator.get_locator(), locator.get_by(), wait_seconds)

    @staticmethod
    def is_element_visible(locator, wait_seconds=10):
        return Searcher.get_driver().is_element_visible(locator.get_locator(), locator.get_by(), wait_seconds)

    @staticmethod
    def is_element_clickable(locator, wait_seconds=10):
        return Searcher.get_driver().is_element_clickable(locator.get_locator(), locator.get_by(), wait_seconds)

    @staticmethod
    def is_alert_present():
        return Searcher.get_driver().is_alert_present()

    @staticmethod
    def alert_accept():
        Searcher.get_driver().alert_accept()

    @staticmethod
    def alert_decline():
        Searcher.get_driver().alert_decline()

    @staticmethod
    def get_alert_text():
        return Searcher.get_driver().get_alert_text()

    @staticmethod
    def long_press_to_element_and_move_to_other_element(from_element, to_element, time_in_seconds):
        Searcher.get_driver().long_press_to_element_and_move_to_other_element(from_element, to_element, time_in_seconds)

    @staticmethod
    def long_press_on_element(element, time_in_seconds):
        Searcher.get_driver().long_press_on_element(element, time_in_seconds)

    @staticmethod
    def put_app_in_background(time_idle=120):
        Searcher.get_driver().put_app_in_background(time_idle)

    @staticmethod
    def __swipe_to(locator, swipe_percent, method, timeout=1, prim_timeout=0, swipes_limit=10):
        for i in range(swipes_limit):
            if i == 0 and prim_timeout != 0:
                if Searcher.is_element_visible(locator, prim_timeout):
                    return True
            if Searcher.is_element_visible(locator, timeout):
                return True
            method(swipe_percent)
        return False

    @staticmethod
    def __swipe_from(locator, swipe_percent, method, timeout=1, prim_timeout=0, swipes_limit=10):
        for i in range(swipes_limit):
            if i == 0 and prim_timeout != 0:
                if not Searcher.is_element_visible(locator, prim_timeout):
                    return True
            if not Searcher.is_element_visible(locator, timeout):
                return True
            method(swipe_percent)
        return False

    @staticmethod
    def swipe_up_to_element(locator, swipe_percent=50, timeout=1, prim_timeout=0, swipes_limit=10):
        return Searcher.__swipe_to(locator, swipe_percent, Searcher.swipe_up, timeout, prim_timeout, swipes_limit)

    @staticmethod
    def swipe_down_to_element(locator, swipe_percent=50, timeout=1, prim_timeout=0, swipes_limit=10):
        return Searcher.__swipe_to(locator, swipe_percent, Searcher.swipe_down, timeout, prim_timeout, swipes_limit)

    @staticmethod
    def swipe_up_from_element(locator, swipe_percent=50, timeout=1, prim_timeout=0, swipes_limit=10):
        return Searcher.__swipe_to(locator, swipe_percent, Searcher.swipe_up, timeout, prim_timeout, swipes_limit)

    @staticmethod
    def swipe_down_from_element(locator, swipe_percent=50, timeout=1, prim_timeout=0, swipes_limit=10):
        return Searcher.__swipe_to(locator, swipe_percent, Searcher.swipe_down, timeout, prim_timeout, swipes_limit)

    @staticmethod
    def swipe_right():
        Searcher.get_driver().swipe_right(Searcher.SWIPE_HORIZONTAL_X, Searcher.SWIPE_HORIZONTAL_Y,
                                          Searcher.SWIPE_HORIZONTAL_MOVE)

    @staticmethod
    def swipe_left():
        Searcher.get_driver().swipe_left(Searcher.SCREEN_WIDTH - 25, Searcher.SWIPE_HORIZONTAL_Y,
                                         Searcher.SWIPE_HORIZONTAL_MOVE)

    @staticmethod
    def swipe_up(swipe_percent=50):
        Searcher.get_driver().swipe_up(Searcher.SWIPE_VERTICAL_X, Searcher.SWIPE_VERTICAL_Y,
                                       Searcher._get_vertical_swipe_move(swipe_percent))

    @staticmethod
    def swipe_down(swipe_percent=50):
        Searcher.get_driver().swipe_down(Searcher.SWIPE_VERTICAL_X, Searcher.SWIPE_VERTICAL_Y,
                                         Searcher._get_vertical_swipe_move(swipe_percent))

    @staticmethod
    def back():
        Searcher.get_driver().back()

    @staticmethod
    def find_element(locator):
        if locator.get_by() == By.XPATH:
            return Searcher.get_driver().find_element_by_xpath(locator.get_locator())
        if locator.get_by() == By.NAME:
            return Searcher.get_driver().find_element_by_name(locator.get_locator())
        raise RuntimeError("unexpected type of locator. currently only XPATH is supported")

    @staticmethod
    def find_elements(locator):
        if locator.get_by() == By.XPATH:
            return Searcher.get_driver().find_elements_by_xpath(locator.get_locator())
        raise RuntimeError("unexpected type of locator. currently only XPATH is supported")

    @staticmethod
    def get_screen_size():
        if Properties.if_ios():
            size = Searcher.get_driver().find_element_by_xpath("//UIAApplication").size
        else:
            size = Searcher.get_driver().find_element_by_xpath("//*").size
        return size

    @staticmethod
    def reset_driver():
        Searcher.get_driver().quit()
        Searcher.driver = None

    @staticmethod
    def set_up(desired_caps):
        Searcher.driver = CustomDriver()
        Searcher.driver.setup(desired_caps)
        time.sleep(5)
        Searcher.SCREEN_SIZE = Searcher.get_screen_size()
        Searcher.SCREEN_WIDTH = Searcher.SCREEN_SIZE["width"]
        Searcher.SCREEN_HEIGHT = Searcher.SCREEN_SIZE["height"]
        width = Searcher.SCREEN_WIDTH
        height = Searcher.SCREEN_HEIGHT
        Searcher.SWIPE_VERTICAL_X = 200
        Searcher.SWIPE_VERTICAL_Y = height / 2
        Searcher.SWIPE_HORIZONTAL_Y = width / 2
        Searcher.SWIPE_HORIZONTAL_X = 25
        Searcher.SWIPE_HORIZONTAL_MOVE = width - width / 10

    @staticmethod
    def _get_vertical_swipe_move(swipe_percent):
        return Searcher.SCREEN_HEIGHT * swipe_percent / 100 - 20

    @staticmethod
    def tap_on_screen_center():
        width = Searcher.SCREEN_WIDTH - Searcher.SCREEN_WIDTH / 2
        height = Searcher.SCREEN_HEIGHT - Searcher.SCREEN_HEIGHT / 2
        Searcher.get_driver().tap([(width, height)], 200)

    @staticmethod
    def tap_on(x, y):
        Searcher.get_driver().tap([(x, y)], 200)

    @staticmethod
    def click_search_button():
        width = Searcher.SCREEN_WIDTH - Searcher.SCREEN_WIDTH / 20
        height = Searcher.SCREEN_HEIGHT - Searcher.SCREEN_HEIGHT / 20
        Searcher.get_driver().tap([(width, height)], 200)

    @staticmethod
    def increase_volume_by_application_button():
        width = Searcher.SCREEN_WIDTH - Searcher.SCREEN_WIDTH / 20
        height = Searcher.SCREEN_HEIGHT - Searcher.SCREEN_HEIGHT / 20
        Searcher.get_driver().tap([(width, height)], 200)

    @staticmethod
    def decrease_volume_by_application_button():
        width = Searcher.SCREEN_WIDTH / 20
        height = Searcher.SCREEN_HEIGHT - Searcher.SCREEN_HEIGHT / 20
        Searcher.get_driver().tap([(width, height)], 200)

    @staticmethod
    def increase_volume_by_device_button():
        Searcher.get_driver().keyevent(Searcher.KEYCODE_VOLUME_UP)

    @staticmethod
    def decrease_volume_by_device_button():
        Searcher.get_driver().keyevent(Searcher.KEYCODE_VOLUME_DOWN)

    @staticmethod
    def get_screenshot():
        Searcher.get_driver().take_screenshot(Properties.get_screenshot_path()+"/1.jpg")
