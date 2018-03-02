from framework_entries.cones import Track

__author__ = 'andrey'

from mobile_ui_entries.impl.InputField import InputField
from mobile_ui_entries.impl.Button import Button
from mobile_ui_entries.impl.WebLink import WebLink
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import SearchPageLocators
from config_entries.Properties import Properties


class SearchPage(BasicPage):
    @staticmethod
    def search_track(search_string):
        InputField(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.searchInput)).send_keys(
            search_string)
        if not Properties.if_ios():
            SearchPage.click_search_button_on_keyboard()

    @staticmethod
    def click_likes():
        Button(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.likes)).click()

    @staticmethod
    def play_this_playlist():
        SearchPage.return_play_this_playlist_button().click()

    @staticmethod
    def swipe_to_play_this_playlist():
        SearchPage.swipe_up_to_element(SearchPage.return_play_this_playlist_button())

    @staticmethod
    def play_this_album():
        Button(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.playThisAlbum)).click()

    @staticmethod
    def click_back():
        Button(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.back)).click()

    @staticmethod
    def click_first_result():
        Button(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.clickFirstResult)).click()

    @staticmethod
    def get_playlist_content():
        """:rtype: list of framework_entries.Track.Track"""
        if Properties.if_ios():
            SearchPage.swipe_to_bottom()
        artists = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.playlistArtist))
        artists_list = artists.get_elements()
        size = len(artists_list)
        songs = []
        if not Properties.if_ios():
            tracks = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.playlistTrack))
            tracks_list = tracks.get_elements()
            for i in range(size):
                songs.append(Track.Track(artists_list[i].text, tracks_list[i].text))
        else:
            for i in range(size):
                songs.append(Track.Track(artists_list[i].text, ""))
        return songs

    @staticmethod
    def get_current_filter_type():
        if Properties.if_ios():
            element = WebLink(
                Properties.get_search_page_locator_map().get_locator(
                    SearchPageLocators.currentSearchType))
            return element.get_elements()[2].get_attribute("name")
        return WebLink(
            Properties.get_search_page_locator_map().get_locator(SearchPageLocators.currentSearchType)).get_text()

    @staticmethod
    def get_next_filter_type():
        return WebLink(
            Properties.get_search_page_locator_map().get_locator(SearchPageLocators.nextSearchType)).get_text()

    @staticmethod
    def swipe_to_bottom():
        SearchPage.swipe_down_to_element(
            WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.pageBottom)))

    @staticmethod
    def is_artists_type_exists():
        if Properties.if_ios():
            return WebLink(
                Properties.get_search_page_locator_map().get_locator(
                    SearchPageLocators.artistsSearchType)).is_presented()
        return SearchPage.swipe_down_to_element(
            WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.artistsSearchType)))

    @staticmethod
    def is_tracks_type_exists():
        if Properties.if_ios():
            return WebLink(
                Properties.get_search_page_locator_map().get_locator(
                    SearchPageLocators.tracksSearchType)).is_presented()
        return SearchPage.swipe_down_to_element(
            WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.tracksSearchType)))

    # workaround method #001, should be deleted eventually
    @staticmethod
    def is_search_result_exists(name):
        if Properties.if_ios():
            return WebLink(
                Properties.get_play_list_page_locator_map().get_locator(
                    SearchPageLocators.resultChooser)).is_presented()
        return SearchPage.swipe_down_to_element(SearchPage.return_search_result(name).click())

    # workaround method #001, should be deleted eventually
    @staticmethod
    def get_artist_from_search(number):
        artists = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.searchArtist))
        artist = artists.get_elements()
        if len(artist) <= number:
            return ''
        if Properties.if_ios():
            return artist[number].get_attribute('name')
        return artist[number].text

    @staticmethod
    def get_album_from_search(number):
        artists = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.searchAlbum))
        artist = artists.get_elements()[number]
        return artist.text

    @staticmethod
    def is_current_filter_type_visible():
        return WebLink(
            Properties.get_search_page_locator_map().get_locator(SearchPageLocators.currentSearchType)).is_visible()

    @staticmethod
    def click_ok_alert_popup():
        return Button(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.okPopUpAlert)).click()

    @staticmethod
    def click_learn_more_alert_popup():
        return Button(
            Properties.get_search_page_locator_map().get_locator(SearchPageLocators.learnMorePopUpAlert)).click()

    @staticmethod
    def choose_filter(name):
        Button(
            Properties.get_search_page_locator_map().get_locator(SearchPageLocators.filter)).click()
        SearchPage.return_filter_option(name).click()

    @staticmethod
    def click_search_result_x(int_x):
        SearchPage.return_search_option(int_x).click()

    @staticmethod
    def return_search_result(name):
        locator = Properties.get_search_page_locator_map().get_locator(SearchPageLocators.resultChooser)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
        return Button(locator)

    @staticmethod
    def return_filter_option(name):
        locator = Properties.get_search_page_locator_map().get_locator(SearchPageLocators.filterChooser)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", name)
        return Button(locator)

    @staticmethod
    def return_search_option(int_x):
        locator = Properties.get_search_page_locator_map().get_locator(SearchPageLocators.clickXResult)
        locator.locator = locator.locator.replace("TEXT_TO_CHANGE", int_x)
        return Button(locator)


    @staticmethod
    def is_filter_type_exists(filter_type):
        if Properties.if_ios():
            element = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.filterSearchType))
            element.locator.locator = element.locator.locator.replace("TEXT_TO_CHANGE", filter_type)
            return element.is_presented()
        return SearchPage.swipe_down_to_element(
            WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.artistsSearchType)))

    @staticmethod
    def is_in_search_results(element1, element2):
        element_counter = 1
        artist = SearchPage.get_artist_from_search(0)
        while artist != '':
            artist = SearchPage.get_artist_from_search(element_counter)
            if artist.__contains__(element1) and artist.__contains__(element2):
                element_counter = -1
                return True
            element_counter += 1

    @staticmethod
    def return_play_this_playlist_button():
        return Button(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.playThisPlaylist))

    @staticmethod
    def return_track_from_playlist(number):
        # 0 Will be played when play_this_playlist clicked, 1 is first in next list
        tracks = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.playlistTrack))
        track = tracks.get_elements()[number]
        return track.text

    @staticmethod
    def return_artist_from_playlist(number):
        # 0 Will be played when play_this_playlist clicked, 1 is first in next list
        artists = WebLink(Properties.get_search_page_locator_map().get_locator(SearchPageLocators.playlistArtist))
        artist = artists.get_elements()[number]
        return artist.text

