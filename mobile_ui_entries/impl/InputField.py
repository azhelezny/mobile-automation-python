__author__ = 'andrey'

from mobile_ui_entries.basics.EditableUiEntry import EditableUiEntry


class InputField(EditableUiEntry):
    def __init__(self, locator):
        EditableUiEntry.__init__(self, locator)
