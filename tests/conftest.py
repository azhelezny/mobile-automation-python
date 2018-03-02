import pytest
import time
from config_entries.Properties import Properties
from framework_entries.cones.Tune import TuneClient
from mobile_ui_pages.ConeSettingsPage import ConeSettingsPage
from mobile_ui_pages.ConesPage import ConesPage
from mobile_ui_pages.MoreInfoPage import MoreInfoPage
from mobile_ui_searcher.Searcher import Searcher
from mobile_ui_pages.SearchPage import SearchPage
from mobile_ui_pages.PlayListPage import PlayListPage
from zephyr.Integration import ZephyrTestOptions, ZephyrManager
from zephyr.zephyr_ci import TestStatus
from framework_scripts import DeviceInstaller

__author__ = 'fedotovp'


@pytest.yield_fixture(scope="module", autouse=True)
def preparation():
    for cone in range(Properties.get_cones().get_size()):
        Properties.get_cones().get_by_number(cone).get_comms_remote().uncluster()
        Properties.get_cones().get_by_number(cone).get_comms_remote().wait_for_unclustering()
        if Properties.if_ios():
            DeviceInstaller.uninstall_app_by_name()
    yield
    Searcher.reset_driver()


@pytest.fixture(scope="module")
def first_cone_tuned(first_cone):
    """:rtype : TuneClient"""
    return first_cone.get_tune_client()


@pytest.fixture(scope="module")
def second_cone_tuned(second_cone):
    """:rtype : TuneClient"""
    return second_cone.get_tune_client()


@pytest.fixture(scope="module")
def free_cone_tuned(free_cone):
    """:rtype : TuneClient"""
    return free_cone.get_tune_client()


@pytest.fixture(scope="module")
def first_cone_journal(first_cone):
    """:rtype : JournalClient"""
    return first_cone.get_journal_client()


@pytest.fixture(scope="module")
def first_cone():
    """:rtype : framework_entries.cones.Cone.Cone"""
    return Properties.get_cones().get_by_number(0)


@pytest.fixture(scope="module")
def second_cone():
    """:rtype : framework_entries.cones.Cone.Cone"""
    return Properties.get_cones().get_by_number(1)


@pytest.fixture(scope="module")
def free_cone():
    """:rtype : framework_entries.cones.Cone.Cone"""
    return Properties.get_cones().get_by_number(2)


@pytest.fixture(scope="module")
def unlim_user():
    """:rtype : config_entries.entries.User.User"""
    return Properties.get_users().get_unlimited()


@pytest.fixture(scope="module")
def free_user():
    """:rtype : config_entries.entries.User.User"""
    return Properties.get_users().get_free()


@pytest.yield_fixture(scope="function")
def search_dialogue():
    PlayListPage.click_on_search()
    yield
    while not PlayListPage.is_this_a_play_list_page():
        if Properties.if_ios():
            SearchPage.click_back()
        else:
            SearchPage.back()
        time.sleep(1)


@pytest.yield_fixture(scope="function")
def exit_volume_dialogue():
    yield
    PlayListPage.tap_on_screen_center()


@pytest.fixture(scope="module")
def play_likes_playlist():
    PlayListPage.click_on_search()
    SearchPage.click_likes()
    tracks = SearchPage.get_playlist_content()
    SearchPage.swipe_to_play_this_playlist()
    SearchPage.play_this_playlist()
    return tracks

# TODO: Fix this shit yo, the x variable is not pulling correct list item of returned appium-elements in the app
@pytest.fixture(scope="module")
def play_x_rdio_playlist(int_x='5'):
    PlayListPage.click_on_search()
    SearchPage.click_search_result_x(int_x)
    tracks = SearchPage.get_playlist_content()
    SearchPage.swipe_to_play_this_playlist()
    SearchPage.play_this_playlist()
    return tracks

@pytest.yield_fixture(scope="function")
def more_info_dialogue():
    yield
    if MoreInfoPage.return_description().is_presented():
        MoreInfoPage.swipe_right()


@pytest.yield_fixture(scope="function")
def unlink_cones():
    for i in range(Properties.get_cones().get_size()):
        cone_comms = Properties.get_cones().get_by_number(i).get_comms_remote()
        if cone_comms.is_clustered():
            cone_comms.uncluster()
    yield
    for i in range(Properties.get_cones().get_size()):
        cone_comms = Properties.get_cones().get_by_number(i).get_comms_remote()
        if cone_comms.is_clustered():
            cone_comms.uncluster()


@pytest.yield_fixture(scope="function")
def cone_settings_exit():
    yield
    ConeSettingsPage.back_click()
    ConesPage.done_click()


# Zephyr integration fixtures

@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    rep = __multicall__.execute()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.yield_fixture(scope="function", autouse=True)
def fin(request):
    yield
    if not ZephyrTestOptions.is_reportable():
        return

    test_end = time.time()
    test_duration = request.node.rep_call.duration
    test_start = test_end - test_duration

    start_time = Properties.get_zephyr_session().get_start_time()
    build = Properties.get_zephyr_session().get_build()
    environment = Properties.get_external_parameters().get_firmware_version()
    test_cases_path = Properties.get_zephyr_session().get_test_cases_root()

    test_name = '%s.%s - %s' % (environment, build, start_time)

    zm = ZephyrManager()
    zm.login()

    test_case_tree = zm.get_test_case_tree(test_cases_path)
    zm.logout()
    ZephyrTestOptions.reset()
    """
    cycle_id = zm.create_test_execution(project, release, test_name, build, environment, start_time, end_time)


    ret = zm.add_phase_to_cycle(test_case_tree, cycle_id, start_time, end_time)

    # Query the cycle so we can get the ID of the phase we added
    cycle = zm.get_cycle_by_id(cycle_id)

    phase_id = zm.get_phase_id_by_cycle_id(phase, cycle_id)

    tests = zm.get_test_schedules_for_phase(phase_id)

    test_data = {}

    for child in root:
        test_status = TestStatus.ChangeStatus
        test_note = ''

        error = child.find('error')
        failure = child.find('failure')

        if error is None and failure is None:
            test_status = TestStatus.Pass
            test_note = 'Passed in %s seconds.' % child.attrib['time']
        else:
            test_status = TestStatus.Fail
            test_note = 'Failed'

        test_data[int(child.attrib['zephyr_tcid'])] = {'status': test_status,
                                                       'note': test_note}

    # zm.update_test_status(tests, test_data)

    zm.logout()

    if request.node.rep_setup.failed:
        print "setting up failed"
    elif request.node.rep_setup.passed:
        # module_name = request.node.fspath.purebasename
        ZephyrTestOptions.set_test_name(request.node.name)
        if request.node.rep_call.failed:
            ZephyrTestOptions.set_status(TestStatus.Fail)
        else:
            ZephyrTestOptions.set_status(TestStatus.Pass)
    """
