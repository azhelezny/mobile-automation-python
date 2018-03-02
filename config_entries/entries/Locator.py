__author__ = 'andrey'

from selenium.webdriver.common.by import By


class Locator:
    def __init__(self, locator, by_str):
        self.locator = locator
        self.by = None
        if by_str.lower().strip() == "xpath":
            self.by = By.XPATH
        elif by_str.lower().strip() == "css":
            self.by = By.CSS_SELECTOR
        elif by_str.lower().strip() == "id":
            self.by = By.ID
        elif by_str.lower().strip() == "name":
            self.by = By.NAME

    def get_locator(self):
        return self.locator

    def get_by(self):
        return self.by

    def __str__(self):
        return "type: " + self.by + "\nlocator: " + self.locator


class LocatorsList:
    def __init__(self, json_dictionary):
        self.locators = json_dictionary

    def get_locator(self, locator_name):
        return Locator(self.locators[locator_name][1], self.locators[locator_name][0])

    def __str__(self):
        result = ""
        for locator in self.locators:
            result += "\n--LOCATOR---\nname: " + locator + "\ntype: " + self.locators[locator][0] + "\nlocator: " + \
                      self.locators[locator][1]
        return result

