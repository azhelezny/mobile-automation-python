""" ONE_LINE_DESCRIPTION
"""
__author__ = "craig"
__copyright__ = "Copyright (c) 2015, Aether Things, Inc. All Rights Reserved."
__license__ = "Commercial Proprietary"


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

"""
def test_log_in(free_user):
    LoginPage.login(free_user.get_login(), free_user.get_password())


def test_choose_cone(free_cone):
    ConesPage.choose_by_name(free_cone.get_name())


def test_rdio_skip_limit(free_cone_tuned):
    PlayListPage.reset_skips_left_count()
    prev_track = free_cone_tuned.get_json_status_track()
    assert PlayListPage.get_skips_left() == 6, "Skip counter did not reset"
    PlayListPage.play_next_track_btn()
    assert not text_utils.smart_compare(free_cone_tuned.get_json_status_track(), prev_track), "Track did not skip"
    assert PlayListPage.get_skips_left() == 5, "Skip counter did not subtract 1 skip"
    PlayListPage.play_next_track_btn()
    assert PlayListPage.get_skips_left() == 4, "Skip counter did not subtract 1 skip"
    PlayListPage.play_next_track_btn()
    assert PlayListPage.get_skips_left() == 3, "Skip counter did not subtract 1 skip"
    PlayListPage.play_next_track_btn()
    assert PlayListPage.get_skips_left() == 2, "Skip counter did not subtract 1 skip"
    PlayListPage.play_next_track_btn()
    time.sleep(5)
    PlayListPage.play_next_track_btn()
    assert PlayListPage.get_skips_left() == 0, "Skip counter did not subtract 1 skip"
    PlayListPage.play_next_track()
    assert PlayListPage.is_alert_present(), "Wrong alert message"
    PlayListPage.alert_accept()
    PlayListPage.play_next_set()
    assert PlayListPage.get_skips_left() == 6, "Skip counter did not reset"


def test_no_selectable_prev_tracks(free_cone_tuned):
    free_cone_tuned.next_set()
    time.sleep(10)
    current_track = free_cone_tuned.get_json_status_track()
    free_cone_tuned.next_track()
    PlayListPage._swipe_to_last_track()
    PlayListPage.return_prev_track_button().click()
    assert PlayListPage.is_alert_present(), "Error, no alert popup for prev tracks"
    PlayListPage.alert_accept()
    assert not text_utils.smart_compare(free_cone_tuned.get_json_status_track(), current_track), "Error, prev track was played"


def test_radio_stream_not_counted():
    skip_count = PlayListPage.get_skips_left()
    search_string = "KQED"
    PlayListPage.click_on_search()
    SearchPage.search_track(search_string)
    SearchPage.choose_filter("radio")
    SearchPage.click_first_result()
    assert PlayListPage.get_skips_left() == skip_count, "Radio stream should NOT remove 'skip' from count"


def test_search_triggered_modal():
    # add fixture to force app out of 'search' page if previous test fails
    PlayListPage.click_on_search()
    search_text = "gold on the ceiling"
    SearchPage.search_track(search_text)
    SearchPage.choose_filter('track')
    SearchPage.is_filter_type_exists('tracks')
    SearchPage.is_search_result_exists('Gold on The Ceiling')
    assert text_utils.smart_compare(PlayListPage.get_alert_text(),
                                    "You'll need an Rdio Unlimited account to request a specific song. Visit"
                                    " rdio.com to upgrade. Meanwhile, Cone will play something similar."), "Wrong " \
                                                                                                           "alert " \
"""                                                                                                           "message"










