# _*_ coding: utf-8 _*_

import time
from framework_entries.cones.Cone import Cones
from general_utils import text_utils
from mobile_ui_pages.ConesPage import ConesPage
from mobile_ui_pages.LoginPage import LoginPage
from mobile_ui_pages.PlayListPage import PlayListPage
from mobile_ui_searcher.Searcher import Searcher
from zephyr.Integration import ZephyrManager


__author__ = 'andrey'

from config_entries.Properties import Properties

zm = ZephyrManager()
zm.login()
zm.__get_projects_list()