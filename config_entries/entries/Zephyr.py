from datetime import datetime

__author__ = 'andrey'


class ZephyrSession:
    def __init__(self, json_representation):
        self.__user_name = json_representation["userName"]
        self.__user_pass = json_representation["userPassword"]
        self.__host = json_representation["host"]
        self.__project = json_representation["project"]
        self.__release = json_representation["release"]
        self.__phase = json_representation["phase"]
        self.__test_case = json_representation["testCasesRoot"]
        self.__build = json_representation["build"]
        self.__start_time = str(datetime.utcnow().strftime('%Y-%m-%d'))

    def get_start_time(self):
        return self.__start_time

    def get_user_name(self):
        return self.__user_name

    def get_user_password(self):
        return self.__user_pass

    def get_url(self):
        return 'http://%s/flex/services/soap/zephyrsoapservice-v1?wsdl' % self.__host

    def get_project(self):
        return self.__project

    def get_release(self):
        return self.__release

    def get_phase(self):
        from config_entries.Properties import Properties
        os_mark = "Android"
        if Properties.if_ios():
            os_mark = "IOS"
        return self.__phase[:2] + [os_mark] + self.__phase[2:]

    def get_test_cases_root(self):
        from config_entries.Properties import Properties
        os_mark = "Android"
        if Properties.if_ios():
            os_mark = "IOS"
        return self.__test_case[:1] + [os_mark] + self.__test_case[1:]

    def get_build(self):
        return self.__build