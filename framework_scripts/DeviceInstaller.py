""" ONE_LINE_DESCRIPTION
"""
__author__ = "Aether Things"
__copyright__ = "Copyright (c) 2015, Aether Things, Inc. All Rights Reserved."
__license__ = "Commercial Proprietary"

import subprocess
from config_entries.Properties import Properties


def uninstall_app_by_name(app_package='com.aether'):
    if Properties.if_ios():
        output = subprocess.Popen(['/usr/local/bin/ideviceinstaller', '-l'], stdout=subprocess.PIPE).communicate()[0]
        if app_package in output:
            subprocess.Popen(['/usr/local/bin/ideviceinstaller', '-U', 'com.aether.cone'], stdout=subprocess.PIPE)
            return True
        else:
            return False
    else:
        output = subprocess.Popen(["adb shell 'pm list packages -f'", " | grep aether"]).communicate()[0]
        if app_package in output:
            subprocess.Popen(['adb uninstall com.aether.aethercone'])
            return True
        else:
            return False


def install_app_by_name(app_package, dir):
    subprocess.Popen(['ideviceinstaller', '-i', dir + '/application-ios.ipa'], stdout=subprocess.PIPE)
    if app_package in subprocess.Popen(['ideviceinstaller', '-l'], stdout=subprocess.PIPE).communicate()[0]:
        return True
    else:
        return False
