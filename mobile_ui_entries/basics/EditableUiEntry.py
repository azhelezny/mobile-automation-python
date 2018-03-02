__author__ = 'andrey'

from mobile_ui_entries.basics.BasicUiEntry import BasicUiEntry


class EditableUiEntry(BasicUiEntry):
    def __init__(self, locator):
        BasicUiEntry.__init__(self, locator)

    def send_keys(self, text):
        self.get_element().send_keys(text)