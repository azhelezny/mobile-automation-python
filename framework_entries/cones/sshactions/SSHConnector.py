from scp import SCPClient

__author__ = 'andrey'
import paramiko
import time


class SSHExecutor():
    def __init__(self, hostname="", login="", password=""):
        self.ssh = paramiko.SSHClient()
        self.host = hostname
        self.login = login
        self.password = password

    def get_user_name(self):
        return self.login

    def get_user_password(self):
        return self.password

    def get_host(self):
        return self.host

    def start_session(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.login, password=self.password)

    def execute_session_command(self, command, timeout=15):
        stdin, stdout, stderr = self.ssh.exec_command(command, timeout=timeout)
        error = stderr.read()
        if error != '':
            raise RuntimeError(
                "ssh SESSION command [" + command + "] was executed with next error message:\n<<<" + error + ">>>")
        return stdout.read()

    def execute_session_command_no_stderr(self, command, timeout=15):
        self.ssh.exec_command(command, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_session()

    def stop_session(self):
        self.ssh.close()

    @staticmethod
    def execute_single_command(hostname, login, password, command, timeout=15):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=login, password=password)
            stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
            error = stderr.read()
            if error != '':
                raise RuntimeError(
                    "ssh SINGLE command [" + command + "] was executed with next error message:\n<<<" + error + ">>>")
            return stdout.read()

    @staticmethod
    def reboot_host(hostname, login, password, timeout=15):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=login, password=password)
            chan = ssh.get_transport().open_session()
            chan.get_pty()
            chan.settimeout(timeout)
            chan.exec_command("sudo reboot")
            time.sleep(5)
            chan.send(password + '\n')
            time.sleep(10)
            chan.close()

    @staticmethod
    def execute_single_sudo_command(hostname, login, password, command, timeout=15):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=login, password=password)
            chan = ssh.get_transport().open_session()
            chan.get_pty()
            chan.settimeout(timeout)
            chan.exec_command(command)
            time.sleep(5)
            read_bytes = 1024
            buf = chan.recv(read_bytes)
            if buf.lower().endswith("password:"):
                chan.send(password + '\n')
            error = chan.recv_stderr(read_bytes)
            if error != '':
                raise RuntimeError(
                    "ssh SINGLE SUDO command [" + command + "] was executed with next error message:\n<<<" + error +
                    ">>>")
            chan.close()
            return chan.recv(read_bytes)

    @staticmethod
    def copy_single_file(hostname, login, password, local_path, remote_path):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=login, password=password)
            scp = SCPClient(ssh.get_transport())
            scp.put(local_path, remote_path)
            return "File [" + local_path + "] was copied to [" + remote_path + "]"

    @staticmethod
    def send_single_file(hostname, login, password, local_path, remote_path):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=login, password=password)
            scp = SCPClient(ssh.get_transport())
            scp.get(remote_path, local_path)
            return "Remote file [" + remote_path + "] was sent to local host [" + local_path + "]"

    @staticmethod
    def read_single_file(hostname, login, password, remote_path):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=login, password=password)
            sftp_client = ssh.open_sftp()
            remote_file = sftp_client.open(remote_path)
            return remote_file
