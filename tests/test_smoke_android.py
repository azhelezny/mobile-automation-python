import time
from framework_entries.cones import EqualizerGains
from mobile_ui_pages.ConeSettingsPage import ConeSettingsPage
from mobile_ui_pages.ConesPage import ConesPage
from mobile_ui_pages.PlayListPage import PlayListPage
from mobile_ui_pages.SearchPage import SearchPage
from mobile_ui_pages.WelcomePage import WelcomePage
from mobile_ui_pages.LoginPage import LoginPage
from general_utils import text_utils
from general_utils import math_utils

__author__ = 'fedotovp'


def test_log_in(unlim_user):
    LoginPage.login(unlim_user.get_login(), unlim_user.get_password())
    assert WelcomePage.get_welcome_message() == "welcome\n" + unlim_user.get_name() + "!", \
        "Wrong welcome page message"


def test_choose_cone(first_cone):
    ConesPage.choose_by_name(first_cone.get_name())


def test_next_set(first_cone_tuned):
    prev_set = first_cone_tuned.get_set()
    next_set = first_cone_tuned.get_next_set()
    prev_track = PlayListPage.get_track()
    prev_artist = PlayListPage.get_artist()
    PlayListPage.play_next_set()
    PlayListPage.wait_for_track_change(prev_track)
    assert not text_utils.smart_compare(PlayListPage.get_track(), prev_track), "Track didn't switch"
    assert not text_utils.smart_compare(PlayListPage.get_artist(), prev_artist), "Artist didn't switch"
    actual = PlayListPage.get_track()
    expected = first_cone_tuned.get_json_status_track()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected
    actual = PlayListPage.get_track()
    expected = first_cone_tuned.get_json_status_track()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected
    actual = first_cone_tuned.get_set()
    assert actual != prev_set, "Set not changed"
    assert actual == next_set, "Wrong next set"


def test_play_list_details(first_cone_tuned):
    actual = PlayListPage.get_artist()
    expected = first_cone_tuned.get_json_status_artist()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing artist on Playlist page, page: " + actual + " cone: " + expected
    actual = PlayListPage.get_track()
    expected = first_cone_tuned.get_json_status_track()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected
    assert PlayListPage.get_playing_from() == "playing from Rdio", \
        "Wrong 'playing from' source on Playlist page"
    actual = PlayListPage.get_similar_to_text()
    expected = "Similar to " + first_cone_tuned.get_json_status_artist()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong 'Similar to' link text on Playlist page, page: " + actual + " expected: " + expected


def test_play(first_cone_tuned):
    PlayListPage.play()
    assert PlayListPage.is_playing(), "Wrong app playing status"
    assert first_cone_tuned.is_playing(), "Wrong cone playing status"


def test_pause(first_cone_tuned):
    PlayListPage.pause()
    assert not PlayListPage.is_playing(), "Wrong app playing status"
    assert first_cone_tuned.is_paused(), "Wrong cone playing status"


def test_play_next_track(first_cone_tuned):
    previous_track = PlayListPage.get_track()
    previous_artist = PlayListPage.get_artist()
    # checking of the next track
    PlayListPage.play_next_track()
    assert PlayListPage.wait_for_track_change(previous_track, 10), "Track never changed"
    actual = PlayListPage.get_track()
    expected = first_cone_tuned.get_json_status_track()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected
    actual = PlayListPage.get_artist()
    expected = first_cone_tuned.get_json_status_artist()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing artist on Playlist page, page: " + actual + " cone: " + expected
    # checking of the previous track
    assert text_utils.smart_compare(PlayListPage.last_track(), previous_track), "Last track not appeared in list"
    assert text_utils.smart_compare(PlayListPage.last_artist(), previous_artist), "Last artist not appeared in list"


def test_volume_change(first_cone_tuned, exit_volume_dialogue):
    first_cone_tuned.set_zero_volume()
    PlayListPage.click_on_change_volume()
    current_volume = 0
    assert first_cone_tuned.get_volume() == 0, "error of changing for cone's volume on the device"
    for i in range(1, 10):
        expected_volume = first_cone_tuned.get_expected_volume_after_changing(0, i)
        PlayListPage.increase_volume_by_application_button()
        current_volume = first_cone_tuned.get_volume()
        assert math_utils.in_range(current_volume, expected_volume, 0.01), "change in volume doesn't affect the cone"
    for i in range(1, 5):
        expected_volume = first_cone_tuned.get_expected_volume_after_changing(current_volume, -1)
        PlayListPage.decrease_volume_by_application_button()
        current_volume = first_cone_tuned.get_volume()
        assert math_utils.in_range(current_volume, expected_volume, 0.01), "change in volume doesn't affect the cone"


def test_search(search_dialogue):
    search_string = "Daft Punk"
    SearchPage.search_track(search_string)
    SearchPage.back()
    time.sleep(5)
    actual = SearchPage.get_artist_from_search(0).__contains__(search_string) or SearchPage.get_album_from_search(
        0).__contains__(search_string)
    assert actual, "No search string in search result"
    SearchPage.swipe_to_bottom()
    assert SearchPage.get_artist_from_search(0).__contains__(search_string), "No search string in search result"


def test_search_filters(search_dialogue):
    SearchPage.search_track("P")
    SearchPage.back()
    time.sleep(5)
    assert SearchPage.get_current_filter_type() == "albums", "Wrong current filter type"
    assert SearchPage.is_artists_type_exists(), "Missing Artists filter type"
    assert SearchPage.is_tracks_type_exists(), "Missing Tracks filter type"
    assert SearchPage.get_current_filter_type() == "artists", "Wrong current filter type"
    SearchPage.swipe_to_bottom()
    # TODO: fix this once Adrian changes podcast/track filtering option
    # assert SearchPage.get_current_filter_type() == "tracks", "Wrong current filter type"


def test_play_from_likes(play_likes_playlist, first_cone_tuned):
    current_track = play_likes_playlist[0].track
    current_artist = play_likes_playlist[0].artist
    assert text_utils.smart_compare(current_artist,
                                    PlayListPage.get_artist()), "Wrong currently playing artist on Playlist page"
    assert text_utils.smart_compare(current_track,
                                    PlayListPage.get_track()), "Wrong currently playing track on Playlist page"
    assert text_utils.smart_compare(PlayListPage.get_artist(),
                                    first_cone_tuned.get_json_status_artist()), "Wrong currently playing artist on cone"
    assert text_utils.smart_compare(PlayListPage.get_track(),
                                    first_cone_tuned.get_json_status_track()), "Wrong currently playing track on cone"


def test_next_track_click_and_previous_element_check(play_x_rdio_playlist, first_cone_tuned):
    previous_track = play_x_rdio_playlist[0].track
    previous_artist = play_x_rdio_playlist[0].artist
    next_playing_track = play_x_rdio_playlist[1].track
    next_playing_artist = play_x_rdio_playlist[1].artist
    # next track in list validation
    assert text_utils.smart_compare(next_playing_track, PlayListPage.next_track()), "Next list wrong track"
    # next track check

    PlayListPage.play_next_artist()
    assert PlayListPage.wait_for_track_change(previous_track), "Track never changed"
    actual = PlayListPage.get_track()
    expected = first_cone_tuned.get_json_status_track()
    assert text_utils.smart_compare(actual, expected), \
        "Currently playing track from cone:  and application are different: " + actual + " cone: " + expected
    assert text_utils.smart_compare(actual, next_playing_track), \
        "Wrong currently playing track on Playlist page: ->" + actual + " expected: " + next_playing_track
    actual = PlayListPage.get_artist()
    assert text_utils.smart_compare(actual, next_playing_artist), \
        "Wrong currently playing artist on Playlist page: ->" + actual + " expected: " + next_playing_artist
    # previous track check
    assert PlayListPage.last_artist() == previous_artist, "Last artist not appeared in list"
    assert PlayListPage.last_track() == previous_track, "Last track not appeared in list"


def test_equalizer_change(first_cone, first_cone_tuned):
    PlayListPage.click_on_cones_list()
    ConesPage.cones_settings_click(first_cone.get_name())
    assert ConeSettingsPage.get_cone_name() == first_cone.get_name(), "Wrong cone settings page"
    new_state = "Classical"
    ConeSettingsPage.set_equalizer(new_state)
    ConeSettingsPage.back()
    ConeSettingsPage.wait_for_equalizer_state(new_state)
    assert ConeSettingsPage.get_eq_status() == new_state, "Wrong eq state in app"
    assert first_cone_tuned.get_gain() == EqualizerGains.CLASSICAL, "Wrong eq state in cone"
    new_state = "Acoustic"
    ConeSettingsPage.set_equalizer(new_state)
    ConeSettingsPage.back()
    ConeSettingsPage.wait_for_equalizer_state(new_state)
    assert ConeSettingsPage.get_eq_status() == new_state, "Wrong eq state in app"
    assert first_cone_tuned.get_gain() == EqualizerGains.ACOUSTIC, "Wrong eq state in cone"
