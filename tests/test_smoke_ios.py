import time
from config_entries.Properties import Properties
from general_utils import math_utils
from mobile_ui_pages.ConesPage import ConesPage
from mobile_ui_pages.ConeSettingsPage import ConeSettingsPage
from mobile_ui_pages.PlayListPage import PlayListPage
from mobile_ui_pages.WelcomePage import WelcomePage
from mobile_ui_pages.LoginPage import LoginPage
from mobile_ui_pages.SearchPage import SearchPage
from mobile_ui_pages.MoreInfoPage import MoreInfoPage
from framework_entries.cones import EqualizerGains
from general_utils import text_utils

__author__ = 'andrey'


def test_log_in(unlim_user):
    LoginPage.login(unlim_user.get_login(), unlim_user.get_password())
    WelcomePage.skip_help()


def test_choose_cone(first_cone):
    ConesPage.choose_by_name(first_cone.get_name())


def test_play(first_cone_tuned):
    PlayListPage.play()
    assert PlayListPage.is_playing(), "Wrong app playing status"
    assert first_cone_tuned.is_playing(), "Wrong cone playing status"


def test_pause(first_cone_tuned):
    PlayListPage.pause()
    assert not PlayListPage.is_playing(), "Wrong app playing status"
    assert first_cone_tuned.is_paused(), "Wrong cone playing status"


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
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected


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
    PlayListPage._swipe_to_similar_to_text()
    actual = PlayListPage.get_similar_to_text()
    expected = "Similar to " + first_cone_tuned.get_json_status_artist()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong 'Similar to' link text on Playlist page, page: " + actual + " expected: " + expected


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
    for i in range(1, 2):
        expected_volume = first_cone_tuned.get_expected_volume_after_changing(current_volume, -1)
        PlayListPage.decrease_volume_by_application_button()
        current_volume = first_cone_tuned.get_volume()
        assert math_utils.in_range(current_volume, expected_volume, 0.01), "change in volume doesn't affect the cone"


def test_search(search_dialogue):
    search_string = "Daft Punk"
    SearchPage.search_track(search_string)
    time.sleep(5)
    actual = SearchPage.get_artist_from_search(0).__contains__(search_string) or SearchPage.get_album_from_search(
        0).__contains__(search_string)
    assert actual, "No search string in search result"
    assert SearchPage.get_artist_from_search(0).__contains__(search_string), "No search string in search result"


def test_search_filters(search_dialogue):
    search_string = "Rock"
    SearchPage.search_track(search_string)
    time.sleep(5)
    assert SearchPage.is_filter_type_exists("artists"), "Missing Artists filter type"
    assert SearchPage.is_filter_type_exists("tracks"), "Missing Tracks filter type"
    SearchPage.choose_filter("track")
    assert SearchPage.is_in_search_results(search_string, "Will"), "Missing tracks with Will and " + search_string
    assert SearchPage.is_filter_type_exists("tracks"), "Missing Tracks filter type"
    assert not SearchPage.is_filter_type_exists("artists"), "Artists filter type presented while should not"
    SearchPage.choose_filter("artist")
    actual = SearchPage.get_artist_from_search(0).__contains__("albums") and SearchPage.get_artist_from_search(
        0).__contains__(search_string)
    assert actual, "No search string in search result!!"
    assert SearchPage.is_filter_type_exists("artists"), "Missing Artists filter type"
    assert not SearchPage.is_filter_type_exists("tracks"), "Tracks filter type presented while should not"
    SearchPage.choose_filter("radio")
    assert SearchPage.is_in_search_results(search_string, "0"), "Missing tracks with 0 and " + search_string
    assert SearchPage.is_filter_type_exists("radio"), "Missing Radio filter type"
    assert not SearchPage.is_filter_type_exists("album"), "Album filter type presented while should not"
    SearchPage.choose_filter("album")
    actual = SearchPage.get_artist_from_search(0).__contains__("tracks") and SearchPage.get_artist_from_search(
        0).__contains__(search_string)
    assert actual, "No search string in search result!!!!"
    assert SearchPage.is_filter_type_exists("album"), "Missing Album filter type"
    assert not SearchPage.is_filter_type_exists("radio"), "Radio filter type presented while should not"
    SearchPage.choose_filter("none")
    assert SearchPage.is_filter_type_exists("artists"), "Missing Artists filter type"
    assert SearchPage.is_filter_type_exists("album"), "Missing Album filter type"
    assert SearchPage.is_filter_type_exists("radio"), "Missing Radio filter type"
    assert SearchPage.is_filter_type_exists("tracks"), "Missing Tracks filter type"


def test_play_from_likes(play_likes_playlist, first_cone_tuned):
    current_artist_expected = play_likes_playlist[0].artist
    current_artist_actual = PlayListPage.get_track() + '\n' + PlayListPage.get_artist()
    assert text_utils.smart_compare(current_artist_expected,
                                    current_artist_actual), "Wrong currently playing artist on Playlist page"
    current_artist_actual = first_cone_tuned.get_json_status_track() + "\n" + first_cone_tuned.get_json_status_artist()
    assert text_utils.smart_compare(current_artist_expected,
                                    current_artist_actual), "Wrong currently playing artist on cone"


def test_next_track_list(play_likes_playlist):
    PlayListPage._swipe_to_current_artist()
    i = 1
    while i < play_likes_playlist.__len__():
        assert text_utils.smart_compare(play_likes_playlist[i].artist,  PlayListPage.next_track(i-1)), "Wrong tack in next tracks playlist"
        i = i + 1

# TODO: figure out what is going on in this test...
def test_play_from_next_list(play_likes_playlist, first_cone_tuned):
    previous_track = PlayListPage.get_track()
    # checking of the next track
    PlayListPage._swipe_to_next_artist()
    # the test failed due to radio not having a 'artist' element and _swipe_to was too big.
    PlayListPage.play_next_track()
    assert PlayListPage.wait_for_track_change(previous_track, 10), "Track never changed"
    actual = PlayListPage.get_track() + "\n" + PlayListPage.get_artist()
    expected = play_likes_playlist[1].artist
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " expected from next list: " + expected
    actual = PlayListPage.get_track()
    expected = first_cone_tuned.get_json_status_track()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected
    actual = PlayListPage.get_artist()
    expected = first_cone_tuned.get_json_status_artist()
    assert text_utils.smart_compare(actual, expected), \
        "Wrong currently playing track on Playlist page, page: " + actual + " cone: " + expected


def test_more_info_page(more_info_dialogue, first_cone_tuned):
    first_cone_tuned.play_track_from_id('rdio://t2748953')  # track: You Never Can Tell (1964 Single Version / Mono)
    PlayListPage.swipe_left()
    # TODO: TUNE-6940, navigation away from cloud search... aka no artist bio info from wikipedia
    # assert MoreInfoPage.get_description().__contains__(
    #     "Chuck" and "born October 18, 1926"), "Incorrect artist description"
    assert text_utils.smart_compare(MoreInfoPage.get_albums_section(), "top albums"), "No top albums section"
    assert MoreInfoPage.get_top_tracks_section().__contains__("top tracks"), "No top tracks section"


def test_equalizer_change(first_cone, first_cone_tuned):
    ConesPage.cones_settings_click(first_cone.get_name())
    assert ConeSettingsPage.get_cone_name() == first_cone.get_name(), "Wrong cone settings page"
    new_state = "Classical"
    old_cone_eq = first_cone_tuned.get_gain()
    ConeSettingsPage.set_equalizer(new_state)
    for i in range(10):
        if not (first_cone_tuned.get_gain() == old_cone_eq):
            break
        time.sleep(1)
    # create app check when bug fixed
    # assert ConeSettingsPage.get_eq_status() == new_state, "Wrong eq state in app"
    assert first_cone_tuned.get_gain() == EqualizerGains.CLASSICAL, "Wrong eq state in cone"
    new_state = "Acoustic"
    old_cone_eq = first_cone_tuned.get_gain()
    ConeSettingsPage.set_equalizer(new_state)
    for i in range(10):
        if not (first_cone_tuned.get_gain() == old_cone_eq):
            break
        time.sleep(1)
    # create app check when bug fixed
    # assert ConeSettingsPage.get_eq_status() == new_state, "Wrong eq state in app"
    assert first_cone_tuned.get_gain() == EqualizerGains.ACOUSTIC, "Wrong eq state in cone"
