""" ONE_LINE_DESCRIPTION
"""
__author__ = "Aether Things"
__copyright__ = "Copyright (c) 2015, Aether Things, Inc. All Rights Reserved."
__license__ = "Commercial Proprietary"

import time
from general_utils import text_utils


class JournalClient():
    LOGGER_LOCATION = '/tmp/cone_logger.txt'
    LOCAL_LOGGER_LOCATION = '/Users/craig/'

    def __init__(self, ssh_connector):
        self.ssh = ssh_connector
        """:type : framework_entries.cones.sshactions.SSHConnector.SSHExecutor"""
        self.host = self.ssh.get_host()
        self.user = self.ssh.get_user_name()
        self.pwd = self.ssh.get_user_password()
        self.ti_host = 0
        self.tf_host = 0
        self.t_host_diff = 0
        self.ti_dut = 0
        self.tf_dut = 0
        self.t_dut_diff = 0
        self.time_lighttp = []
        self.time_lighttp_angel = []

    def start_logger(self):
        self.ssh.execute_session_command_no_stderr('journalctl -f -o short-precise > %s'%JournalClient.LOGGER_LOCATION)
        self.ti_host = self.set_host_time()

    def stop_logger(self):
        self.ssh.execute_session_command("ps | grep -i journalctl | awk '{print $1}' | xargs | awk '{print $1}' | xargs kill -9")
        self.tf_host = self.set_host_time()
        time.sleep(1)
        self.ssh.execute_session_command("ps | grep -i journalctl | awk '{print $1}' | xargs | awk '{print $1}' | xargs kill -9")
        if self.ti_host != 0:
            self.t_host_diff = self.tf_host - self.ti_host


    def copy_remote_log_file(self, remote_path=LOGGER_LOCATION, local_path=LOCAL_LOGGER_LOCATION):
        self.ssh.send_single_file(self.host, self.user, self.pwd, local_path, remote_path)

    def clear_log_file(self):
        try:
            self.ssh.execute_session_command("rm %s"%JournalClient.LOGGER_LOCATION)
        except:
            "There was no log file to remove from %s"%JournalClient.LOGGER_LOCATION

    def check_log_for_arc_http(self):
        self.copy_remote_log_file()
        lines = open('/Users/craig/cone_logger.txt')
        self.get_ti_dut()
        self.get_tf_dut()
        self.t_dut_diff = self.tf_dut - self.ti_dut
        assert self.t_dut_diff > 0.0
        for line in lines:
            self.get_arc_over_cloud_time(line)
            self.get_arc_over_lan_time(line)

    def set_host_time(self):
        return int(round(time.time()))

    def get_arc_over_lan_time(self,line):
        if "lighttpd[" in line:
            self.time_lighttp.append(text_utils.return_log_time_ms(line))
            return True

    def get_arc_over_cloud_time(self,line):
        if "lighttpd-angel[" in line:
            self.time_lighttp_angel.append(text_utils.return_log_time_ms(line))
            return True

    def get_time_delta_dut(self):
        self.get_ti_dut()
        self.get_tf_dut()
        if self.tf_dut < self.ti_dut:
            raise AssertionError("Final dut time cannot be less than initial dut time")

    def get_ti_dut(self, log_file=LOCAL_LOGGER_LOCATION):
        with open(log_file + 'cone_logger.txt') as lines:
            next(lines)
            for line in lines:
                if text_utils.return_log_time_ms(line):
                    self.ti_dut = text_utils.return_log_time_ms(line)
                    return

    def get_tf_dut(self, log_file=LOCAL_LOGGER_LOCATION):
        with open(log_file + 'cone_logger.txt') as lines:
            lines.seek(-1024, 2)
            line = lines.readlines()[-1].decode()
            if text_utils.return_log_time_ms(line):
                self.tf_dut = text_utils.return_log_time_ms(line)
                return


