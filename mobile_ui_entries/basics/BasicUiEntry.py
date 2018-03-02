from mobile_ui_searcher.Searcher import Searcher

__author__ = 'andrey'


class BasicUiEntry(object):
    def __init__(self, locator):
        self.locator = locator
        self.element = None

    def get_element(self):
        """:rtype: appium.webdriver.webelement.WebElement"""
        self.element = Searcher.find_element(self.locator)
        return self.element

    def get_elements(self):
        """:rtype: list of appium.webdriver.webelement.WebElement"""
        return Searcher.find_elements(self.locator)

    def get_location(self):
        return self.get_element().location

    def get_size(self):
        return self.get_element().size

    def get_text(self):
        return self.get_element().text

    def get_attribute(self, attr_name):
        return self.get_element().get_attribute(attr_name)

    def is_visible(self, time_to_wait=10):
        return Searcher.is_element_visible(self.locator, time_to_wait)

    def is_presented(self, time_to_wait=10):
        return Searcher.is_element_presented(self.locator, time_to_wait)

    def is_clickable(self, time_to_wait=10):
        return Searcher.is_element_clickable(self.locator, time_to_wait)
