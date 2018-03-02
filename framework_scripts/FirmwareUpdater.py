__author__ = 'andrey'

import traceback

from config_entries import Properties


exit_code = 0

for i in range(Properties.Properties.get_cones().get_size()):
    try:
        Properties.Properties.get_cones().get_by_number(i).get_firmware().update_firmware()
    except Exception:
        traceback.print_exc()
        exit_code = 3

exit(exit_code)