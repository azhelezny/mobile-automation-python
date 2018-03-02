__author__ = 'andrey'

import os
import time


class Firmware:
    def __init__(self, ssh_connector):
        self.firmware_remote_dir = "/tmp/firmware"
        self.ssh = ssh_connector
        """:type : framework_entries.cones.sshactions.SSHConnector.SSHExecutor"""
        self.host = self.ssh.get_host()
        self.user = self.ssh.get_user_name()
        self.pwd = self.ssh.get_user_password()

        from config_entries import Properties
        self.local_firmware_dir = Properties.Properties.get_firmware_path()
        self.desired_firmware_version = Properties.Properties.get_external_parameters().get_firmware_version().upper()

    def execute_command(self, command):
        return self.ssh.execute_single_command(self.host, self.user, self.pwd, command)

    def execute_sudo_command(self, command, timeout=15):
        return self.ssh.execute_single_sudo_command(self.host, self.user, self.pwd, command, timeout)

    def get_version(self):
        return self.execute_command("bash -l -c 'echo $VERSION'").split(":")[1]

    def check_version(self):
        current_version = self.get_version().lower().strip()
        expected_version = self.desired_firmware_version.lower().strip()
        print "current version: "+current_version
        print "expected version: "+expected_version
        return current_version == expected_version

    def update_firmware(self):
        if not self.check_version():
            print self.execute_command("rm -rf " + self.firmware_remote_dir + "; echo directory was deleted")
            print self.execute_command("mkdir -p " + self.firmware_remote_dir + "; echo directory was created")
            print self.ssh.copy_single_file(self.host, self.user, self.pwd,
                                            self.local_firmware_dir + "/" + self.desired_firmware_version + ".morse",
                                            self.firmware_remote_dir)
            print self.execute_sudo_command(
                "sudo sysupdate -p " + self.firmware_remote_dir + "/" + self.desired_firmware_version + ".morse",
                timeout=180)
            print self.ssh.reboot_host(self.host, self.user, self.pwd)

            time.sleep(20)

            retries_count = 10
            delay = 10

            for i in range(retries_count + 1):
                if i == retries_count:
                    raise RuntimeError("Host is unavailable after installing of new firmware")
                a = os.system("ping -c 1 " + self.host)
                if a != 0:
                    time.sleep(delay)
                else:
                    break

            # host should be available but ssh daemon can be not started
            time.sleep(40)

            if not self.check_version():
                raise RuntimeError("Firmware wasn't updated successfully, look device's logs for details")