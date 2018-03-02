from config_entries.Properties import Properties
from zephyr.Integration import ZephyrTestOptions

__author__ = 'andrey'


def test_1():
    ZephyrTestOptions.add_test_group("Smoke").set_tcid("285")
    pass


def test_2():
    assert 0