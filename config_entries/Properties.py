from config_entries.entries.Zephyr import ZephyrSession

__author__ = 'andrey'

import json
import os

from config_entries.entries.ExternalProperties import *
from config_entries.entries.User import Users, User
from framework_entries.cones.Cone import Cones, Cone
from config_entries.entries.Locator import *


class Properties:
    properties_path = os.getenv("FRAMEWORK_HOME", "/Users/andrey/automation_tests/LohikaPlayground/resources1")
    application_ios_name = "application-ios.ipa"
    application_android_name = "application-android.apk"
    external_parameters = None
    desired_capabilities = None
    zephyr_session = None
    users = None
    cones = None

    locators_login_page = None
    locators_welcome_page = None
    locators_main_page = None
    locators_play_list_page = None
    locators_cones_page = None
    locators_search_page = None
    locators_cone_settings_page = None
    locators_user_properties_page = None
    locators_more_info_page = None

    @staticmethod
    def _get_sum_for_version(version_string, is_desired_capabilities_mode=False):
        parsed_version_string = version_string
        if is_desired_capabilities_mode:
            parsed_version_string = version_string.split("_")[1]
        elements = parsed_version_string.split(".")
        result = 0
        coefficient = 1
        for i in range(len(elements) - 1, -1, -1):
            result += int(elements[i]) * coefficient
            coefficient *= 10
        return result

    @staticmethod
    def _get_closest_version(data_dict):
        desired_version = Properties.get_external_parameters().get_desired_os_version()
        desired_os = Properties.get_external_parameters().get_desired_os()
        desired_capabilities_mode = data_dict.keys()[0].__contains__("_")
        matched_versions = []
        for i in data_dict:
            if i.__contains__(desired_version):
                if desired_capabilities_mode and not i.__contains__(desired_os):
                    continue
                matched_versions.append(i)
        mvl = len(matched_versions)
        if mvl == 0:
            raise RuntimeError(
                "unable to find desired version [" + desired_version + "] in content <<" + data_dict + ">>")
        maximum = Properties._get_sum_for_version(matched_versions[0], desired_capabilities_mode)
        result_index = 0
        for i in range(1, mvl):
            current = Properties._get_sum_for_version(matched_versions[i], desired_capabilities_mode)
            if maximum < current:
                maximum = current
                result_index = i
        return matched_versions[result_index]

    @staticmethod
    def get_screenshot_path():
        return Properties.properties_path + "/screenshots"

    @staticmethod
    def get_applications_path():
        return Properties.properties_path + "/applications"

    @staticmethod
    def if_ios():
        return Properties.get_external_parameters().desired_os.lower() == "ios"

    @staticmethod
    def get_firmware_path():
        return Properties.get_applications_path() + "/firmware"

    @staticmethod
    def get_android_application_path():
        return Properties.get_applications_path() + "/android"

    @staticmethod
    def get_ios_application_path():
        return Properties.get_applications_path() + "/ios"

    @staticmethod
    def get_external_parameters():
        """:rtype : ExternalProperties"""
        if Properties.external_parameters is None:
            with open(Properties.properties_path + "/external/external.json") as raw_json:
                Properties.external_parameters = ExternalProperties(json.load(raw_json))
        return Properties.external_parameters

    @staticmethod
    def get_zephyr_session():
        """:rtype : ZephyrSession"""
        if Properties.zephyr_session is None:
            with open(Properties.properties_path + "/external/zephyr.json") as raw_json:
                Properties.zephyr_session = ZephyrSession(json.load(raw_json))
        return Properties.zephyr_session

    @staticmethod
    def get_desired_capabilities():
        if Properties.desired_capabilities is None:
            with open(Properties.properties_path + "/capabilities/desiredCapabilities.json") as raw_json:
                data = json.load(raw_json)
                os_type = Properties.get_external_parameters().get_desired_os()
                os_ver = Properties._get_closest_version(data)
                Properties.desired_capabilities = data[os_ver]
                Properties.desired_capabilities["platformName"] = os_type
                Properties.desired_capabilities["platformVersion"] = os_ver.split("_")[1]
                if Properties.if_ios():
                    if Properties.desired_capabilities["app"] == "":
                        Properties.desired_capabilities[
                            "app"] = Properties.get_ios_application_path() + "/" + Properties.application_ios_name
                else:
                    Properties.desired_capabilities[
                        "app"] = Properties.get_android_application_path() + "/" + Properties.application_android_name
        return Properties.desired_capabilities

    @staticmethod
    def get_cones():
        """:rtype : Cones"""
        if Properties.cones is None:
            with open(Properties.properties_path + "/external/cones.json") as raw_json:
                data = json.load(raw_json)
                cones_json_list = data["cones"]
                Properties.cones = Cones()
                for cone in cones_json_list:
                    Properties.cones.add_cone(Cone(cone))
        return Properties.cones

    @staticmethod
    def get_users():
        """:rtype : Users"""
        if Properties.users is None:
            with open(Properties.properties_path + "/external/credentials.json") as raw_json:
                data = json.load(raw_json)
                users_json_list = data["users"]
                Properties.users = Users()
                for user in users_json_list:
                    Properties.users.add_user(User(user))
        return Properties.users


    @staticmethod
    def _get_page_locators_from_file(file_name):
        locators_dir = os.path.abspath(os.path.dirname(__file__)) + "/../resources/locators/"
        extended_file_name = ""
        if Properties.get_external_parameters().get_desired_os().lower() == "android":
            extended_file_name += file_name + "Android.json"
        else:
            extended_file_name += file_name + "Ios.json"
        with open(locators_dir + extended_file_name) as raw_json:
            data = json.load(raw_json)
            data = data[Properties._get_closest_version(data)]
        return LocatorsList(data)

    @staticmethod
    def get_login_page_locator_map():
        if Properties.locators_login_page is None:
            Properties.locators_login_page = Properties._get_page_locators_from_file("loginPage")
        return Properties.locators_login_page

    @staticmethod
    def get_welcome_page_locator_map():
        if Properties.locators_welcome_page is None:
            Properties.locators_welcome_page = Properties._get_page_locators_from_file("welcomePage")
        return Properties.locators_welcome_page

    @staticmethod
    def get_cone_settings_page_locator_map():
        if Properties.locators_cone_settings_page is None:
            Properties.locators_cone_settings_page = Properties._get_page_locators_from_file("coneSettingsPage")
        return Properties.locators_cone_settings_page

    @staticmethod
    def get_search_page_locator_map():
        if Properties.locators_search_page is None:
            Properties.locators_search_page = Properties._get_page_locators_from_file("searchPage")
        return Properties.locators_search_page

    @staticmethod
    def get_cones_page_locator_map():
        if Properties.locators_cones_page is None:
            Properties.locators_cones_page = Properties._get_page_locators_from_file("conesPage")
        return Properties.locators_cones_page

    @staticmethod
    def get_play_list_page_locator_map():
        if Properties.locators_play_list_page is None:
            Properties.locators_play_list_page = Properties._get_page_locators_from_file("playListPage")
        return Properties.locators_play_list_page

    @staticmethod
    def get_user_properties_page_locator_map():
        if Properties.locators_user_properties_page is None:
            Properties.locators_user_properties_page = Properties._get_page_locators_from_file("userPropertiesPage")
        return Properties.locators_play_list_page

    @staticmethod
    def get_more_info_page_locator_map():
        if Properties.locators_more_info_page is None:
            Properties.locators_more_info_page = Properties._get_page_locators_from_file("moreInfoPage")
        return Properties.locators_more_info_page
