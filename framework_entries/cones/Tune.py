import time
import json
from general_utils import text_utils

__author__ = 'andrey'


class Tune:
    pass


class TuneClient():
    VOLUME_APPLICATION_STEP_ANDROID = 0.05
    VOLUME_APPLICATION_STEP_IOS = 0.0492

    def __init__(self, ssh_connector):
        self.ssh = ssh_connector
        """:type : framework_entries.cones.sshactions.SSHConnector.SSHExecutor"""

    def is_playing(self):
        return self.ssh.execute_session_command("tune-client playback-state").strip().lower() == "playing"

    def is_paused(self):
        return self.ssh.execute_session_command("tune-client playback-state").strip().lower() == "paused"

    def is_stopped(self):
        return self.ssh.execute_session_command("tune-client playback-state").strip().lower() == "stopped"

    def play(self):
        self.ssh.execute_session_command("tune-client play")

    def stop(self):
        self.ssh.execute_session_command("tune-client stop")

    def pause(self):
        self.ssh.execute_session_command("tune-client pause")

    def next_track(self):
        self.ssh.execute_session_command("tune-client next")

    def next_set(self):
        self.ssh.execute_session_command("tune-client next-set")

    def back(self):
        self.ssh.execute_session_command("tune-client back")

    def play_track_from_id(self,id):
        self.ssh.execute_session_command("tune-client play %s"%id)

    def get_json_status(self):
        return json.loads(self.ssh.execute_session_command("tune-client status-json"))

    def get_json_status_track(self):
        return text_utils.get_json_key_value(self.get_json_status, "title")

    def get_json_status_artist(self):
        return text_utils.get_json_key_value(self.get_json_status, "artist")

    def get_gain(self):
        time.sleep(2)
        return self.ssh.execute_session_command("tune-client gain").split("Gain: ")[1].strip()

    def get_volume(self):
        """:rtype:float"""
        time.sleep(0.7)
        return float(self.ssh.execute_session_command("tune-client volume").split(":")[1].strip())

    def set_volume(self, volume):
        self.ssh.execute_session_command("tune-client volume " + format(volume))
        time.sleep(3)

    def set_middle_volume(self):
        self.set_volume(0.5)

    def set_zero_volume(self):
        self.set_volume(0.0)

    def get_expected_volume_after_changing(self, volume, steps=1):
        result = steps * TuneClient.VOLUME_APPLICATION_STEP_ANDROID
        from config_entries.Properties import Properties

        if Properties.if_ios():
            # volume changes on 3 db by step in ios
            result = steps * TuneClient.VOLUME_APPLICATION_STEP_IOS
        return volume + result

    def get_set(self):
        return self.ssh.execute_session_command("tune-client set").strip()

    def get_next_set(self):
        current_set = self.ssh.execute_session_command("tune-client set").strip()
        sets = self.ssh.execute_session_command("tune-client lssets").split("\n")
        return sets[sets.index(current_set) + 1]

    def wait_for_track_change(self, old_track_name, retries=5):
        for i in range(retries):
            if not text_utils.smart_compare(old_track_name, self.get_json_status_track()):
                return True
            time.sleep(1)
        return False

    def get_provider_info(self,provider,key):
        content_provider = self.ssh.execute_session_command("tune-client provider-info").replace("'",'"')\
            .replace("<","").replace(">","").splitlines()
        for line in content_provider:
            if line.__contains__(provider):
                _line = "{" + line[line.find("{")+1:line.find("}")] + "}"
                _line = json.loads(_line)
                return _line[key]
