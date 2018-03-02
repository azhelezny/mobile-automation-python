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

__author__ = 'fedotovp'


def test_log_in(unlim_user):
    LoginPage.login(unlim_user.get_login(), unlim_user.get_password())
    WelcomePage.skip_help()


def test_dummy_test(first_cone, second_cone):
    # Todo Dummy test should be removed after Clustering in Client works after log in.
    ConesPage.swipe_down()
    first = first_cone.get_comms_client().get_device_id()
    second = second_cone.get_comms_client().get_device_id()
    cones = Properties.get_cones()
    size = cones.get_size()
    master = None
    slave = None
    if first_cone.get_comms_remote().is_slave():
        second_cone.get_comms_remote().uncluster()
    if second_cone.get_comms_remote().is_slave():
        first_cone.get_comms_remote().uncluster()
    for i in range(size):
        if cones.get_by_number(i).get_comms_remote().is_master():
            master = cones.get_by_number(i)
        if cones.get_by_number(i).get_comms_remote().is_slave():
            slave = cones.get_by_number(i)
    if master is None:
        first_cone.get_comms_remote().cluster(first, second)
        return
    master.get_comms_remote().uncluster2(master.get_comms_client().get_device_id(),
                                         slave.get_comms_client().get_device_id())


def test_multicone_link(first_cone, second_cone):
    # Link cones check
    first = first_cone.get_name()
    second = second_cone.get_name()
    if first_cone.get_comms_remote().is_clustered():
        ConesPage.unlink_cones(first, second)
        assert first_cone.get_comms_remote().wait_for_clustering_state_change(True, 10), "Preparation step failed"
    ConesPage.link_cones(first, second)

    first_cone.get_comms_remote().wait_for_clustering_state_change(False, 10)

    assert first_cone.get_comms_remote().is_clustered(), "Cone " + first + " not clustered"
    assert second_cone.get_comms_remote().is_clustered(), "Cone " + second + " not clustered"


def test_multicone_unlink(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    # UnLink cones check
    first = first_cone.get_name()
    second = second_cone.get_name()
    if not first_cone.get_comms_remote().is_clustered():
        ConesPage.link_cones(first, second)
        assert first_cone.get_comms_remote().wait_for_clustering_state_change(False, 10), "Preparation step failed"
    ConesPage.unlink_cones(first, second)
    first_cone.get_comms_remote().wait_for_clustering_state_change(True, 10)
    assert not first_cone.get_comms_remote().is_clustered(), "Cone " + first + " not clustered"
    assert not second_cone.get_comms_remote().is_clustered(), "Cone " + second + " not clustered"

    # When unclustered cones should play unicue content
    first = first_cone_tuned.get_json_status_artist()
    second = second_cone_tuned.get_json_status_artist()
    assert not text_utils.smart_compare(first, second), \
        "Cones playing same content after unclustering"


def test_link_from_cone_settings(first_cone, first_cone_tuned, second_cone, second_cone_tuned, cone_settings_exit):
    # Link cones check
    first = first_cone.get_name()
    second = second_cone.get_name()
    if first_cone.get_comms_remote().is_clustered():
        ConesPage.unlink_cones(first, second)
        assert first_cone.get_comms_remote().wait_for_unclustering(), "Preparation step failed"
    ConesPage.cones_settings_click(first_cone.get_name())
    ConeSettingsPage.link_click(second_cone.get_name())

    assert first_cone.get_comms_remote().is_clustered(), "Cone " + first + " not clustered"
    assert second_cone.get_comms_remote().is_clustered(), "Cone " + second + " not clustered"


def test_unlink_from_cone_settings(first_cone, first_cone_tuned,second_cone, second_cone_tuned, cone_settings_exit):
    first = first_cone.get_name()
    second = second_cone.get_name()
    if not first_cone.get_comms_remote().is_clustered():
        ConesPage.link_cones(first, second)
        assert first_cone.get_comms_remote().wait_for_clustering_state_change(False, 10), "Preparation step failed"
    ConesPage.cones_settings_click(first_cone.get_name())
    ConeSettingsPage.link_click(second_cone.get_name())
    assert not first_cone.get_comms_remote().is_clustered(), "Cone " + first + " not clustered"
    assert not second_cone.get_comms_remote().is_clustered(), "Cone " + second + " not clustered"


def test_play_on_separately(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    first = first_cone.get_name()
    second = second_cone.get_name()
    if first_cone.get_comms_remote().is_clustered():
        ConesPage.unlink_cones(first, second)

    ConesPage.choose_by_name(first_cone.get_name())
    PlayListPage.play()
    ConesPage.choose_by_name(second_cone.get_name())
    PlayListPage.play()
    assert first_cone_tuned.is_playing(), "First cone is not playing"
    assert second_cone_tuned.is_playing(), "Second cone is not playing"
    assert first_cone_tuned.get_json_status_track() is not second_cone_tuned.get_json_status_track(), "Cones play the same track"


def test_link_second_as_master(first_cone, second_cone, first_cone_tuned, second_cone_tuned):
    # UnLink cones check
    first = first_cone.get_name()
    second = second_cone.get_name()
    if first_cone.get_comms_remote().is_clustered():
        ConesPage.unlink_cones(first, second)
        assert first_cone.get_comms_remote().wait_for_unclustering(), "Preparation step failed"
    ConesPage.link_cones(second, first)
    assert first_cone.get_comms_remote().wait_for_clustering(), "Clustering failed"
    assert first_cone.comms_remote.is_slave(), "First cone is not Slave"
    assert second_cone.comms_remote.is_master(), "Second cone is not Master"