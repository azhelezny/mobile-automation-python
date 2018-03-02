from config_entries.Properties import Properties
from config_entries.page_locators.PageLocators import MoreInfoPageLocators
from mobile_ui_entries.impl.WebLink import WebLink
from mobile_ui_pages.BasicPage import BasicPage

__author__ = 'alexanderuvarov'


class MoreInfoPage(BasicPage):
    @staticmethod
    def get_description():
        return MoreInfoPage.return_description().get_attribute("name")

    @staticmethod
    def get_albums_section():
        return MoreInfoPage.return_top_albums_section().get_attribute("name")

    @staticmethod
    def get_top_tracks_section():
        return MoreInfoPage.return_top_tracks_section().get_attribute("name")

    @staticmethod
    def return_description():
        return WebLink(Properties.get_more_info_page_locator_map().get_locator(MoreInfoPageLocators.artistDescription))

    @staticmethod
    def return_top_tracks_section():
        return WebLink(Properties.get_more_info_page_locator_map().get_locator(MoreInfoPageLocators.topTracks))

    @staticmethod
    def return_top_albums_section():
        return WebLink(Properties.get_more_info_page_locator_map().get_locator(MoreInfoPageLocators.topAlbums))