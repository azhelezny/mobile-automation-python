__author__ = 'andrey'

from mobile_ui_entries.basics.BasicUiEntry import BasicUiEntry


class ClickableUiEntry(BasicUiEntry):
    def __init__(self, locator):
        BasicUiEntry.__init__(self, locator)

    def click(self):
        self.get_element().click()
