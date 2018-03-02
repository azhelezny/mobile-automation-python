import json
import time

__author__ = 'andrey'


class CommsClient():
    def __init__(self, ssh_connector):
        self.ssh = ssh_connector
        """:type : framework_entries.cones.sshactions.SSHConnector.SSHExecutor"""

    def get_device_id(self):
        return self.ssh.execute_session_command("comms-client device-id").split("Device-id:")[1].strip()


class CommsRemote():
    def __init__(self, ssh_connector, id):
        self.id = id
        self.ssh = ssh_connector
        """:type : framework_entries.cones.sshactions.SSHConnector.SSHExecutor"""

    def get_cluster_map(self):
        return json.loads(
            self.ssh.execute_session_command("comms-remote cluster-map").replace("<", "").replace(">", "").split(
                "cluster-map:")[1].replace("\'", "\""))

    def get_cone_role(self):
        return self.get_cluster_map()[self.id]["role"]

    def is_master(self):
        return self.get_cluster_map()[self.id]["role"].__contains__("master")

    def is_slave(self):
        return self.get_cluster_map()[self.id]["role"].__contains__("slave")

    def is_clustered(self):
        return self.is_slave() or self.is_master()

    def wait_for_clustering_state_change(self, old_clusterted_state, retries=5):
        for i in range(retries):
            if not old_clusterted_state == self.is_clustered():
                return True
            time.sleep(1)
        return False

    def wait_for_unclustering(self, retries=10):
        for i in range(retries):
            if not self.is_clustered():
                return True
            time.sleep(1)
        return False

    def wait_for_clustering(self, retries=10):
        for i in range(retries):
            if self.is_clustered():
                return True
            time.sleep(1)
        return False

    def uncluster(self):
        # todo delete assert
        self.ssh.execute_session_command("comms-remote uncluster")
        self.wait_for_clustering_state_change(False)

    def cluster(self, cone1_id, cone2_id):
        # todo clustering between current cone and list of cone ids from the parameter
        # todo delete assert
        self.ssh.execute_session_command("comms-remote cluster-create " + cone1_id + " " + cone2_id)
        self.wait_for_clustering_state_change(True)

    def uncluster2(self,cone1_id, cone2_id):
        self.ssh.execute_session_command("comms-remote cluster-remove " + cone1_id + " " + cone2_id)
        self.wait_for_clustering_state_change(False)


