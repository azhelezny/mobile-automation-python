from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from config_entries.Properties import Properties
from appium.webdriver.common.touch_action import TouchAction

__author__ = 'andrey'


class CustomDriver(webdriver.Remote):
    def __init__(self):
        self.driver = None
        """:type: appium.webdriver.Remote"""
        self.driver_wait = None
        """:type: selenium.webdriver.support.ui.WebDriverWait"""
        self.alert_wait = None
        self.session_id = None

    def long_press_to_element_and_move_to_other_element(self, from_element, to_element, time_in_seconds):
        touch_action = TouchAction(self.driver)
        touch_action.long_press(from_element).wait(time_in_seconds * 1000).move_to(to_element).wait(
            1000).release().perform()

    def long_press_on_element(self, element, time_in_seconds):
        touch_action = TouchAction(self.driver)
        touch_action.long_press(element).wait(time_in_seconds * 1000)
        touch_action.perform()

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe_up(self, x, y, distance):
        self.swipe(x, y, x, y + distance)

    def swipe_down(self, x, y, distance):
        self.swipe(x, y, x, y - distance)

    def swipe_left(self, x, y, distance):
        self.swipe(x, y, x - distance, y)

    def swipe_right(self, x, y, distance):
        self.swipe(x, y, x + distance, y)

    def find_element_by_xpath(self, xpath):
        # if self.driver_wait.until(EC.presence_of_element_located((By.XPATH, xpath))):
        #   return self.driver.find_element_by_xpath(xpath)
        return self.driver_wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def find_element_by_name(self, name):
        # if self.driver_wait.until(EC.presence_of_element_located((By.NAME, name))):
        #    return self.driver.find_element_by_name(name)
        return self.driver_wait.until(EC.presence_of_element_located((By.NAME, name)))

    def find_elements_by_xpath(self, xpath):
        if self.driver_wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath))):
            return self.driver.find_elements_by_xpath(xpath)

    def put_app_in_background(self, time_idle):
        self.driver.background_app(time_idle)

    def setup(self, desired_caps, driver_wait_time=30, alert_wait_time=15):
        self.driver = webdriver.Remote(Properties.get_external_parameters().get_remote_server_url(), desired_caps)
        self.driver_wait = WebDriverWait(self.driver, driver_wait_time)
        self.alert_wait = WebDriverWait(self.driver, alert_wait_time)

    def is_alert_present(self):
        try:
            self.alert_wait.until(EC.alert_is_present())
            return True
        except RuntimeError:
            return False

    def get_alert(self):
        alert = None
        if self.is_alert_present():
            alert = self.driver.switch_to.alert()
        return alert

    def get_alert_text(self):
        alert = self.get_alert()
        if alert is not None:
            return alert.text
        return ''

    def alert_accept(self):
        alert = self.get_alert()
        if alert is not None:
            alert.accept()

    def alert_decline(self):
        alert = self.get_alert()
        if alert is not None:
            alert.decline()

    def is_element_presented(self, locator, by=By.XPATH, wait_seconds=15):
        try:
            availability_wait = WebDriverWait(self.driver, wait_seconds)
            availability_wait.until(EC.presence_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator, by=By.XPATH, wait_seconds=15):
        try:
            availability_wait = WebDriverWait(self.driver, wait_seconds)
            availability_wait.until(EC.visibility_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator, by=By.XPATH, wait_seconds=15):
        try:
            availability_wait = WebDriverWait(self.driver, wait_seconds)
            availability_wait.until(EC.element_to_be_clickable((by, locator)))
            return True
        except TimeoutException:
            return False

    def back(self):
        self.driver.back()

    def keyevent(self, keycode, metastate=None):
        return self.driver.keyevent(keycode, metastate)

    def tap(self, positions, duration=None):
        return self.driver.tap(positions, duration)

    def quit(self):
        if self.driver is not None:
            self.driver.quit()

    def take_screenshot(self, file_name):
        return self.driver.get_screenshot_as_file(file_name)
