import time
from general_utils import text_utils

__author__ = 'fedotovp'

from mobile_ui_entries.impl.InputField import InputField
from mobile_ui_pages.BasicPage import BasicPage
from config_entries.page_locators.PageLocators import PlayListPageLocators
from config_entries.Properties import Properties
from mobile_ui_entries.impl.Button import Button
from mobile_ui_entries.impl.WebLink import WebLink


class PlayListPage(BasicPage):
    # business logic - only it should be used inside of tests

    @staticmethod
    def wait_for_track_change(old_track, retries=10):
        for i in range(retries):
            if PlayListPage.return_current_track_input().is_visible():
                if not text_utils.smart_compare(old_track, PlayListPage.get_track()):
                    return True
            time.sleep(1)
        return False

    @staticmethod
    def reset_skips_left_count(retries=5):
        for i in range(retries):
            if not PlayListPage.get_skips_left() == 6:
                PlayListPage.play_next_set()
            else:
                return True
            time.sleep(1)
        return False

    @staticmethod
    def play_pause():
        PlayListPage.return_play_pause_button().click()

    @staticmethod
    def get_artist():
        if not Properties.if_ios():
            PlayListPage._swipe_to_current_artist()
        return PlayListPage.return_current_artist_input().get_text()

    @staticmethod
    def get_track():
        if not Properties.if_ios():
            PlayListPage._swipe_to_current_artist()
        return PlayListPage.return_current_track_input().get_text()

    @staticmethod
    def get_similar_to_text():
        if not Properties.if_ios():
            PlayListPage._swipe_to_similar_to_text()
        return PlayListPage.return_similar_to_text_input().get_text()

    @staticmethod
    def get_skips_left():
        if not Properties.if_ios():
            PlayListPage._swipe_to_similar_to_text()
        else:
            PlayListPage._swipe_to_next_track_btn()
        skip_field = PlayListPage.return_next_track_skips_left().get_text().encode('ascii','ignore')
        if skip_field == "You have no skips left":
            return 0
        else:
            return int(skip_field[9:11])

    @staticmethod
    def get_playing_from():
        return PlayListPage.return_playing_from_input().get_text()

    @staticmethod
    def play_next_track():
        PlayListPage._swipe_to_similar_to_text()
        PlayListPage.return_next_track_button().click()

    @staticmethod
    def play_next_track_btn():
        PlayListPage._swipe_to_next_track_btn()
        PlayListPage.return_next_track_button().click()
        time.sleep(2)

    @staticmethod
    def play_next_set():
        if not Properties.if_ios():
            PlayListPage._swipe_to_next_set()
            PlayListPage.return_next_set_button().click()
        else:
            PlayListPage._swipe_to_similar_to_text()
            PlayListPage.swipe_down()

    @staticmethod
    def _swipe_to_current_artist():
        PlayListPage._swipe_to_similar_to_text()
        PlayListPage.swipe_up_to_element(PlayListPage.return_current_artist_input())

    @staticmethod
    def _swipe_to_similar_to_text():
        PlayListPage.swipe_down_to_element(PlayListPage.return_similar_to_text_input(), 20)

    @staticmethod
    def _swipe_to_next_set():
        PlayListPage.swipe_down_to_element(PlayListPage.return_next_set_button())

    @staticmethod
    def _swipe_to_last_artist():
        PlayListPage._swipe_to_current_artist()
        PlayListPage.swipe_up()
        PlayListPage.swipe_up_to_element(Button(Properties.get_play_list_page_locator_map().
                                                get_locator(PlayListPageLocators.prevArtists)))

    @staticmethod
    def _swipe_to_last_track():
        if not Properties.if_ios():
            PlayListPage._swipe_to_current_artist()
        PlayListPage.swipe_up()
        PlayListPage.swipe_up_to_element(Button(Properties.get_play_list_page_locator_map().
                                                get_locator(PlayListPageLocators.prevTracks)))

    @staticmethod
    def _swipe_to_next_artist():
        PlayListPage._swipe_to_current_artist()
        PlayListPage.swipe_down_to_element(
            Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTracks)))

    @staticmethod
    def _swipe_to_next_track():
        PlayListPage._swipe_to_current_artist()
        PlayListPage.swipe_down_to_element(
            Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTracks)))

    @staticmethod
    def _swipe_to_next_track_btn():
        PlayListPage.swipe_down_to_element(
            Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTrackBtn)),
            swipe_percent=25)

    @staticmethod
    def play():
        assert PlayListPage.return_play_pause_button().is_visible(), "Missing play button on UI(Wrong page maybe?)"
        if PlayListPage.return_play_button().is_visible():
            PlayListPage.return_play_button().click()

    @staticmethod
    def pause():
        assert PlayListPage.return_play_pause_button().is_visible(), "Missing play button on UI(Wrong page maybe?)"
        if PlayListPage.return_pause_button().is_visible():
            PlayListPage.return_pause_button().click()

    @staticmethod
    def is_playing():
        assert PlayListPage.return_play_pause_button().is_visible(), "Missing play button on UI(Wrong page maybe?)"
        return PlayListPage.return_pause_button().is_visible()

    @staticmethod
    def last_artist():
        if not Properties.if_ios():
            PlayListPage._swipe_to_last_artist()
        artists = WebLink(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.prevArtists))
        artist = artists.get_elements()[artists.get_elements().__len__() - 1]
        return artist.text

    @staticmethod
    def last_track():
        PlayListPage._swipe_to_last_track()
        tracks = WebLink(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.prevTracks))
        track = tracks.get_elements()[tracks.get_elements().__len__() - 1]
        return track.text

    @staticmethod
    def next_track(number=0):
        if not Properties.if_ios():
            PlayListPage._swipe_to_next_track()
        tracks = WebLink(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTracks))
        track = tracks.get_elements()[number]
        return track.text

    @staticmethod
    def next_artist(number=0):
        if not Properties.if_ios():
            PlayListPage._swipe_to_next_artist()
        artists = WebLink(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTracks))
        artist = artists.get_elements()[number]
        return artist.text

    @staticmethod
    def play_next_artist(number=0):
        if not Properties.if_ios():
            PlayListPage._swipe_to_next_artist()
        artists = WebLink(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTracks))
        artist = artists.get_elements()[number]
        artist.click()


    @staticmethod
    def click_on_change_volume():
        Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.volumeButton)).click()
        time.sleep(1)

    @staticmethod
    def increase_volume_by_application_button(taps_quantity=1):
        if Properties.if_ios():
            for i in range(taps_quantity):
                Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.increaseVolumeButton)).click()
        else:
            PlayListPage._increase_volume_by_application_button(taps_quantity)

    @staticmethod
    def decrease_volume_by_application_button(taps_quantity=1):
        if Properties.if_ios():
            for i in range(taps_quantity):
                Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.decreaseVolumeButton)).click()
        else:
            PlayListPage._decrease_volume_by_application_button(taps_quantity)

    @staticmethod
    def click_on_search():
        Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.searchBtn)).click()

    @staticmethod
    def click_on_cones_list():
        Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.conesListBtn)).click()

    @staticmethod
    def is_this_a_play_list_page():
        return PlayListPage.return_play_pause_button().is_visible()

    @staticmethod
    def dismiss_alert():
        BasicPage.alert_decline()

    @staticmethod
    def alert_accept():
        BasicPage.alert_accept()

    @staticmethod
    def is_alert_present():
        return BasicPage.is_alert_present()

    @staticmethod
    def alert_accept_alt():
        Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.acceptAlert)).click()

    # elements

    @staticmethod
    def return_play_pause_button():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.playPauseButton))

    @staticmethod
    def return_play_button():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.playButton))

    @staticmethod
    def return_pause_button():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.pauseButton))

    @staticmethod
    def return_current_artist_input():
        return InputField(
            Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.currentTrackArist))

    @staticmethod
    def return_current_track_input():
        return InputField(
            Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.currentTrackName))

    @staticmethod
    def return_similar_to_text_input():
        return InputField(
            Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTrackSimilarToTxt))

    @staticmethod
    def return_playing_from_input():
        return InputField(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.playingFrom))

    @staticmethod
    def return_prev_track_button():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.prevTracks))

    @staticmethod
    def return_next_track_button():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTrackBtn))

    @staticmethod
    def return_next_track_skips_left():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.nextTrackSkipsLeft))

    @staticmethod
    def return_next_set_button():
        return Button(Properties.get_play_list_page_locator_map().get_locator(PlayListPageLocators.somethingDifferent))

    @staticmethod
    def return_alert_text():
        return InputField(BasicPage.get_alert_text())
