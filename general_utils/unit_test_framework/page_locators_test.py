""" ONE_LINE_DESCRIPTION
"""
__author__ = "craig"
__copyright__ = "Copyright (c) 2015, Aether Things, Inc. All Rights Reserved."
__license__ = "Commercial Proprietary"

import json
import os


class Platform:

    page_locators_directory = '/Users/craig/git/automation_tests/LohikaPlayground/resources/locators'
    pages = None


    def __init__(self):
        self.os_type = None
        self.versions = []
        self.pages = []
        self.elements = []

    def add_version(self,version):
        self.versions.append(version)

    def add_pages(self,page):
        self.pages.append(page)

    def add_elements(self,element):
        self.elements.append(element)


    @staticmethod
    def get_all_locator_files():
        files = [f for f in os.listdir(Platform.page_locators_directory) if
                os.path.isfile(os.path.join(Platform.page_locators_directory, f))]
        return files

    @staticmethod
    def get_all_os_version_from_locator_files():
        locator_files = Platform.get_all_locator_files()
        ios = {"versions" : [],
               "pages" : [],
               "elements" : []}
        android = {"versions" : [],
               "pages" : [],
               "elements" : []}
        for page in locator_files:
            plat = None
            suffix = ""
            if "ios" in page.lower():
                plat = ios
                suffix = "_ios"
                num = -12
            elif "android" in page.lower():
                plat = android
                suffix = "_android"
                num = -16
            plat['pages'].append(page[:num] + suffix)
            with open(Platform.page_locators_directory + '/' + page) as raw_json:
                data = json.load(raw_json)
                for key, value in data.iteritems():
                    if key not in plat['versions']:
                        plat['versions'].append(key)
                        for element in data[key]:
                            plat['elements'] = data[key][element]


                    for app_os in [android,ios]:
                        for element in plat[key]:
                            app_os['elements'] = data[key]


        print 'blah'



Platform.get_all_os_version_from_locator_files()
