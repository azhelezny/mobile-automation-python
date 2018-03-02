""" ONE_LINE_DESCRIPTION
"""
__author__ = "Aether Things"
__copyright__ = "Copyright (c) 2015, Aether Things, Inc. All Rights Reserved."
__license__ = "Commercial Proprietary"

from time import sleep
"""

def test_cone_logger(first_cone_journal):
    first_cone_journal.clear_log_file()
    first_cone_journal.start_logger()
    sleep(10)
    # SOME COMMAND OVER LAN SHOULD OCCUR HERE
    first_cone_journal.stop_logger()



def test_read_logger(first_cone_journal):
    first_cone_journal.check_log_for_arc_http()
    sleep(2)
"""