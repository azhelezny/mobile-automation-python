from suds.client import Client
from config_entries.Properties import Properties

__author__ = 'andrey'


class BulkAssigns:
    Creator, Anyone, Individual = range(1, 4)


class TestStatus:
    ChangeStatus, Pass, Fail, WIP, Blocked = range(0, 5)


class ZephyrTestOptions:
    __tcid = None
    __test_name = None
    __test_status = None
    __test_group = []
    __do_report = False

    @staticmethod
    def is_reportable():
        return ZephyrTestOptions.__do_report

    @staticmethod
    def reset():
        ZephyrTestOptions.__tcid = None
        ZephyrTestOptions.__test_name = None
        ZephyrTestOptions.__test_status = None
        ZephyrTestOptions.__test_group = []
        ZephyrTestOptions.__do_report = False

    @staticmethod
    def set_tcid(tcid):
        ZephyrTestOptions.__tcid = tcid
        ZephyrTestOptions.__do_report = True
        return ZephyrTestOptions

    @staticmethod
    def set_test_name(name):
        ZephyrTestOptions.__name = name
        ZephyrTestOptions.__do_report = True
        return ZephyrTestOptions

    @staticmethod
    def add_test_group(group_name):
        ZephyrTestOptions.__test_group.append(group_name)
        ZephyrTestOptions.__do_report = True
        return ZephyrTestOptions

    @staticmethod
    def set_status(status):
        ZephyrTestOptions.__test_status = status
        ZephyrTestOptions.__do_report = True
        return ZephyrTestOptions

    @staticmethod
    def get_test_group():
        return ZephyrTestOptions.__test_group


class ZephyrManager:
    def __init__(self):
        self.user_name = Properties.get_zephyr_session().get_user_name()
        self.password = Properties.get_zephyr_session().get_user_password()
        self.url = Properties.get_zephyr_session().get_url()
        self.client = Client(self.url)
        self.session = None

    def get_search_criteria(self, property_name, operation, value):
        sc = self.client.factory.create('ns0:remoteCriteria')
        sc.searchName = property_name
        sc.searchOperation = operation
        sc.searchValue = value
        return sc

    def login(self):
        self.session = self.client.service.login(self.user_name, self.password)

    def logout(self):
        self.client.service.logout(self.session)
        self.session = None

    def get_project(self):
        project = Properties.get_zephyr_session().get_project()
        sc = self.get_search_criteria('', '', '')
        projects_list = self.client.service.getProjectsByCriteria(sc, 'true', self.session)
        for element in projects_list:
            if element.name == project:
                return element
        raise RuntimeError(
            "Zephyr integration error, unable to find project [" + project + "] in list " + projects_list.__str__())

    def get_release(self):
        release = Properties.get_zephyr_session().get_release()
        project = self.get_project()
        sc = self.get_search_criteria('', '', '')
        rr = self.client.service.getReleasesByCriteria(sc, 'true', self.session)
        for key in rr:
            if key.remoteProjectData.remoteData.name == project.name and key.name == release:
                return key
        raise RuntimeError(
            "Zephyr integration error, unable to find release [" + release + "] in list " + releases.__str__())

    def get_test_case(self, release_id, test_case_id):
        remote_criteria = []
        sc0 = self.get_search_criteria('releaseId', 'EQUALS', release_id)
        sc1 = self.get_search_criteria('id', 'EQUALS', test_case_id)
        remote_criteria.append(sc0)
        remote_criteria.append(sc1)
        return self.client.service.getTestCaseByCriteria(remote_criteria, False, self.session)

    def create_test_execution(self, name, start_date, end_date):
        ret = 0
        try:
            rel_id = self.get_release()
            cycle = self.client.factory.create('remoteCycle')
            cycle.name = name
            cycle.build = Properties.get_zephyr_session().get_build()
            cycle.environment = Properties.get_external_parameters().get_firmware_version()
            cycle.startDate = start_date
            cycle.endDate = end_date
            cycle.releaseId = rel_id
            ret = self.client.service.createNewCycle(cycle, self.session)
        except Exception as e:
            print 'Error creating new test cycle: %s' % e
        return ret

    def create_phase(self, release_id, name, description, parent):
        ret = 0
        phase = self.client.factory.create('remoteRepositoryTree')
        phase.type = 'Phase'
        phase.name = name
        phase.description = description
        phase.releaseId = release_id
        if parent is None:
            phase.parent = parent

        self.client.service.createNewTestcaseTree(phase, self.session)

        return ret

    def check_testcase_sibling(self, search_result_id, sibling_name):
        sc0 = self.get_search_criteria("id", "EQUALS", search_result_id)
        search_criteria = [sc0]
        result = self.client.service.getTestCaseTreesByCriteria(search_criteria, False, self.session)
        categories = result[0].categories
        for category in categories:
            if category.name == sibling_name:
                return category.id
        raise RuntimeError("Unable to find sibling [" + sibling_name + "] inside of testcase: " + result.__str__())

    def get_test_case_tree(self, repo_folders):
        full_path_to_test_case = repo_folders + ZephyrTestOptions.get_test_group()
        release_id = self.get_release().id
        n = len(full_path_to_test_case)
        top_level_name = full_path_to_test_case[0]

        sc0 = self.get_search_criteria("releaseId", "EQUALS", release_id)
        sc1 = self.get_search_criteria("name", "EQUALS", top_level_name)
        remote_criteria = [sc0, sc1]

        top_level_units = self.client.service.getTestCaseTreesByCriteria(remote_criteria, False, self.session)
        if len(top_level_units) > 1 or len(top_level_units) == 0:
            raise RuntimeError("Found several top level unit test cases, or search result is empty, test cases: " +
                               top_level_units.__str__() + " search criteria: " + remote_criteria.__str__())
        if n == 1:
            return top_level_units[0]

        current_test_case_id = top_level_units[0].id
        for i in range(1, n):
            current_test_case_id = self.check_testcase_sibling(current_test_case_id, full_path_to_test_case[i])

        sc0 = self.get_search_criteria("id", "EQUALS", current_test_case_id)
        remote_criteria = [sc0]
        return self.client.service.getTestCaseTreesByCriteria(remote_criteria, False, self.session)

    def add_phase_to_cycle(self, test_cases, cycle_id, start_date, end_date):

        new_phase = self.client.factory.create('remotePhase')
        new_repo = self.client.factory.create('remoteNameValue')
        new_cycle = self.client.factory.create('remoteNameValue')

        new_repo.remoteData.id = test_cases[0].id
        new_cycle.remoteData.id = cycle_id

        new_phase.remoteRepository = new_repo
        new_phase.remoteCycle = new_cycle
        new_phase.startDate = start_date
        new_phase.endDate = end_date

        return self.client.service.addPhaseToCycle(new_phase, BulkAssigns.Anyone, self.session)

    def get_cycle_by_id(self, cycle_id):
        return self.client.service.getCycleById(cycle_id, self.session)

    def get_phase_id_by_cycle_id(self, phase_name, cycle_id):
        ret = -1
        cycle = self.client.service.getCycleById(cycle_id, self.session)

        for phase in cycle.remotePhases:
            if phase.remoteRepository.remoteData.name == phase_name:
                ret = phase.id
                break

        return ret

    def get_test_schedules_for_phase(self, phase_id):
        criteria = []

        sc0 = self.client.factory.create('ns0:remoteCriteria')
        sc0.searchName = 'cyclePhaseId'
        sc0.searchOperation = 'EQUALS'
        sc0.searchValue = phase_id

        criteria.append(sc0)

        return self.client.service.getTestSchedulesByCriteria(criteria, False, self.session)

    def update_test_status(self, test_schedules, test_results):
        update_test_results = []

        for curr_test in test_schedules:
            if curr_test.remoteTestcaseId in test_results:
                tr = self.client.factory.create('remoteTestResult')
                tr.executionNotes = test_results[curr_test.remoteTestcaseId]['note']
                tr.executionStatus = test_results[curr_test.remoteTestcaseId]['status']
                tr.releaseTestScheduleId = curr_test.testScheduleId

                update_test_results.append(tr)

        if len(update_test_results) > 0:
            self.client.service.updateTestStatus(update_test_results, self.session)