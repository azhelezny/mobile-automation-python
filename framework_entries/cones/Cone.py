__author__ = 'andrey'

from framework_entries.cones import Tune
from framework_entries.cones import Comms
from framework_entries.cones import Journal
from framework_entries.cones.sshactions import SSHConnector
from framework_entries.cones import Firmware


class Cone:
    def __init__(self, json_dict):
        self.name = json_dict["name"]
        self.host = json_dict["host"]
        self.user_name = json_dict["userName"]
        self.user_pass = json_dict["userPass"]
        """:type : framework_entries.cones.sshactions.SSHConnector.SSHExecutor"""
        self.ssh = SSHConnector.SSHExecutor(self.host, self.user_name, self.user_pass)
        self.ssh.start_session()

        """:type: framework_entries.cones.Tune.TuneClient"""
        self.tune_client = Tune.TuneClient(self.ssh)
        """:type: framework_entries.cones.Comms.CommsClient"""
        self.comms_client = Comms.CommsClient(self.ssh)
        self.id = self.comms_client.get_device_id()
        """:type: framework_entries.cones.Comms.CommsRemote"""
        self.comms_remote = Comms.CommsRemote(self.ssh, self.id)
        """:type: framework_entries.cones.Comms.Journal.JournalClient"""
        self.journal_client = Journal.JournalClient(self.ssh)
        """:type: framework_entries.cones.Comms.Firmware.Firmware"""
        self.firmware = Firmware.Firmware(self.ssh)

    def get_name(self):
        return self.name

    def get_host(self):
        return self.host

    def get_id(self):
        return self.id

    def get_tune_client(self):
        """:rtype: framework_entries.cones.Tune.TuneClient"""
        return self.tune_client

    def get_journal_client(self):
        """:rtype: framework_entries.cones.Journal.JournalClient"""
        return self.journal_client

    def get_firmware(self):
        """:rtype: framework_entries.cones.Firmware.Firmware"""
        return self.firmware

    def get_comms_remote(self):
        """:rtype: framework_entries.cones.Comms.CommsRemote"""
        return self.comms_remote

    def get_comms_client(self):
        """:rtype: framework_entries.cones.Comms.CommsClient"""
        return self.comms_client

    def close_session(self):
        self.ssh.stop_session()

    def __str__(self):
        return "name: " + self.name + "\nhost: " + self.host + "\nuser: " + self.user_name


class Cones:
    def __init__(self):
        self.cones = []

    def get_size(self):
        return len(self.cones)

    def add_cone(self, cone):
        self.cones.append(cone)

    def get_by_name(self, name):
        """:rtype : Cone"""
        for cone in self.cones:
            if cone.get_name == name:
                return cone
        raise RuntimeError("cone: " + name + " wasn't found in list:" + self.cones.__str__())

    def get_by_number(self, number_in_array):
        """:rtype : Cone"""
        if 0 > number_in_array or number_in_array >= self.get_size():
            raise RuntimeError("cones list has only [" + format(self.get_size()) + "] elements")
        return self.cones[number_in_array]

    def __str__(self):
        result = ""
        for cone in self.cones:
            result += "--CONE--\n" + cone.__str__() + "\n"
        return result