__author__ = 'andrey'

from mobile_ui_pages.BasicPage import BasicPage
from mobile_ui_entries.impl.Button import Button


class MainPage(BasicPage):

    @staticmethod
    def return_cone_button_by_name(name_of_cone):
        return Button(".//*[contains(@resource-id,'tunedevice_ind_cell_np_text')]")

    @staticmethod
    def choose_cone(name_of_cone):
        MainPage.return_cone_button_by_name(name_of_cone).click()