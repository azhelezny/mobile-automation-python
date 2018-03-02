__author__ = 'andrey'

from mobile_ui_entries.basics.ClickableUiEntry import ClickableUiEntry


class Button(ClickableUiEntry):
    def __init__(self, locator):
        ClickableUiEntry.__init__(self, locator)