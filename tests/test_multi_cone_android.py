import time
from config_entries.Properties import Properties
from mobile_ui_pages.ConeSettingsPage import ConeSettingsPage
from mobile_ui_pages.ConesPage import ConesPage
from mobile_ui_pages.PlayListPage import PlayListPage
from mobile_ui_pages.SearchPage import SearchPage
from mobile_ui_pages.WelcomePage import WelcomePage
from mobile_ui_pages.LoginPage import LoginPage
from general_utils import text_utils
from general_utils import math_utils

__author__ = 'alexanderuvarov'


def test_log_in(unlim_user):
    LoginPage.login(unlim_user.get_login(), unlim_user.get_password())
    assert WelcomePage.get_welcome_message() == "welcome\n" + unlim_user.get_name() + "!", \
        "Wrong welcome page message"


def test_link_cone(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if first_cone.comms_remote.is_clustered() and second_cone.comms_remote.is_clustered():
        ConesPage.unlink_cones_by_unlink_group(first_cone.get_name())
    ConesPage.link_cones(first_cone.get_name(), second_cone.get_name())
    assert ConesPage.is_master() and ConesPage.is_slave(), "Cones are not clustered in UI"
    assert first_cone.comms_remote.is_master(), "First cone is not Master"
    assert second_cone.comms_remote.is_slave(), "Second cone is not Slave"


def test_unlink_cone_by_unlink_group(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if not first_cone.comms_remote.is_clustered() and not second_cone.comms_remote.is_clustered():
        ConesPage.link_cones(first_cone.get_name(), second_cone.get_name())
    ConesPage.unlink_cones_by_unlink_group(first_cone.get_name())
    assert not ConesPage.is_master() and not ConesPage.is_slave(), "Cones are  clustered in UI"
    assert not first_cone.comms_remote.is_clustered(), "First cone is not Master"
    assert not second_cone.comms_remote.is_clustered(), "Second cone is not Slave"


def test_unlink_cone_by_unlink_cone(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if not first_cone.comms_remote.is_clustered() and not second_cone.comms_remote.is_clustered():
        ConesPage.link_cones(first_cone.get_name(), second_cone.get_name())
    ConesPage.unlink_cones_by_unlink_cone(second_cone.get_name())
    assert not ConesPage.is_master() and not ConesPage.is_slave(), "Cones are  clustered in UI"
    assert not first_cone.comms_remote.is_clustered(), "First cone is not Master"
    assert not second_cone.comms_remote.is_clustered(), "Second cone is not Slave"


def test_unlink_cone(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if not first_cone.comms_remote.is_clustered() and not second_cone.comms_remote.is_clustered():
        ConesPage.link_cones(first_cone.get_name(), second_cone.get_name())
    ConesPage.unlink_cones(first_cone.get_name(), second_cone.get_name())
    assert not ConesPage.is_master() and not ConesPage.is_slave(), "Cones are clustered in UI"
    assert not first_cone.comms_remote.is_clustered(), "First cone is not Master"
    assert not second_cone.comms_remote.is_clustered(), "Second cone is not Slave"


def test_play_on_cluster(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if not first_cone.comms_remote.is_clustered() and not second_cone.comms_remote.is_clustered():
        ConesPage.link_cones(first_cone.get_name(), second_cone.get_name())
    assert ConesPage.is_master() and ConesPage.is_slave(), "Cones are not clustered in UI"
    ConesPage.choose_by_name(first_cone.get_name())
    PlayListPage.play()
    assert first_cone.comms_remote.is_clustered() and second_cone.comms_remote.is_clustered(), "Cones are not clustered"
    assert first_cone_tuned.is_playing(), "First cone is not playing"
    assert second_cone_tuned.is_paused(), "Second cone is not paused"
    ConesPage.choose_by_name(second_cone.get_name())
    PlayListPage.pause()
    assert not PlayListPage.is_playing(), "Paused"
    assert first_cone_tuned.is_paused(), "First cone is playing"
    PlayListPage.play()
    assert PlayListPage.is_playing(), "Playing"
    assert first_cone_tuned.is_playing(), "First cone is not playing"
    assert second_cone_tuned.is_paused(), "Second cone is not paused"


def test_play_on_separately(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if not first_cone.comms_remote.is_clustered() and not second_cone.comms_remote.is_clustered():
        ConesPage.link_cones(first_cone.get_name(), second_cone.get_name())
    ConesPage.unlink_cones_by_unlink_group(first_cone.get_name())
    ConesPage.choose_by_name(first_cone.get_name())
    PlayListPage.play()
    ConesPage.choose_by_name(second_cone.get_name())
    PlayListPage.play()
    assert first_cone_tuned.is_playing(), "First cone is not playing"
    assert second_cone_tuned.is_playing(), "Second cone is not playing"
    assert first_cone_tuned.get_json_status_track() is not second_cone_tuned.get_json_status_track(), "Cones play the same track"


def test_link_second_as_master(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    if first_cone.comms_remote.is_clustered() and second_cone.comms_remote.is_clustered():
        ConesPage.unlink_cones_by_unlink_group(first_cone.get_name())
    ConesPage.link_cones(second_cone.get_name(), first_cone.get_name())
    assert ConesPage.is_master() and ConesPage.is_slave(), "Cones are not clustered in UI"
    assert first_cone.comms_remote.is_slave(), "First cone is not Slave"
    assert second_cone.comms_remote.is_master(), "Second cone is not Master"