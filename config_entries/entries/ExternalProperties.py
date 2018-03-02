__author__ = 'andrey'


class ExternalProperties():
    def __init__(self, json_representation):
        self.json_representation = json_representation
        self.desired_os = json_representation["desiredOs"]
        self.desired_os_version = json_representation["desiredOsVersion"]
        self.firmware_version = json_representation["firmwareVersion"]
        self.remote_server_url = json_representation["remoteServerUrl"]

    def get_desired_os(self):
        return self.desired_os

    def get_desired_os_version(self):
        return self.desired_os_version

    def get_firmware_version(self):
        return self.firmware_version

    def get_remote_server_url(self):
        return self.remote_server_url

    def __str__(self):
        result = ""
        for line in self.json_representation:
            result += line+"->"+self.json_representation[line]+"\n"
        return result.strip()