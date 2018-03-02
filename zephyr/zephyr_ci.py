# Provides utility functions for interacting with remote Zephyr servers
#
# Author: Rick Mellor, Aether Things, Inc.
#
# Documentation found @ bottom of https://morseproject.atlassian.net/wiki/pages/viewpage.action?pageId=59310134

import sys
import os.path
from suds.client import Client
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


def main():
    url = ''
    username = ''
    password = ''
    build_num = ''
    xunit_path = ''
    test_case_tree = None

    start_time = str(datetime.utcnow().strftime('%Y-%m-%d'))
    end_time = str((datetime.utcnow() + timedelta(days=4)).strftime('%Y-%m-%d'))

    if len(sys.argv) < 11:
        print 'Usage: zephyr_ci.py --host [HOST] --uname [username] --pword [password] --build [buildnum] --xunit [path]'
        exit(1)
    else:
        url = 'http://%s/flex/services/soap/zephyrsoapservice-v1?wsdl' % sys.argv[2]
        username = sys.argv[4]
        password = sys.argv[6]
        build_num = sys.argv[8]
        xunit_path = sys.argv[10]

    if not os.path.isfile(xunit_path):
        print 'Error -- Could not find xunit file: %s' % xunit_path
        exit(1)

    tree = ET.parse(xunit_path)
    root = tree.getroot()

    project = root.attrib['zephyr_project']
    phase = root.attrib['zephyr_phase']
    release = root.attrib['zephyr_release']
    build = root.attrib['zephyr_fw_ver']
    environment = root.attrib['zephyr_environment']
    test_name = '%s.%s - %s' % (environment, build_num, start_time)
    # root.attrib['name']

    zm = ZephyrManager(username, password, url)

    zm.login()

   # user_list = zm.get_user_list()
   # print '\n\nUser List: %s' % len(user_list)
   # for key in user_list:
   #     print 'username: %s, id: %d, email: %s' % (key.username, key.id, key.email)

    projects_list = zm.get_projects_list()
   # print '\nProjects List: %s' % len(user_list)
    for key in projects_list:
        print 'project: %s, id: %d, start: %s' % (key.name, key.id, key.startDate)

        releases_list = zm.get_releases_for_project(key.name)

        for rels in releases_list:
            print '  release: %s, id: %d' % (rels.name, rels.id)

            if key.name == project:
                if rels.name == release:
                    #zm.create_phase(rels.id, 'New Test Phase', 'Created by Python via SOAP', None)

                    test_case_tree = zm.get_test_case_tree(rels.id, phase)
                    pass

    cycle_id = zm.create_test_execution(project, release, test_name, build, environment, start_time, end_time)

    ret = zm.add_phase_to_cycle(test_case_tree, cycle_id, start_time, end_time)

    # Query the cycle so we can get the ID of the phase we added
    cycle = zm.get_cycle_by_id(cycle_id)

    phase_id = zm.get_phase_id_by_cycle_id(phase, cycle_id)

    tests = zm.get_test_schedules_for_phase(phase_id)

    test_data = {}

    for child in root:
        test_status = TestStatus.ChangeStatus
        test_note = ''

        error = child.find('error')
        failure = child.find('failure')

        if error is None and failure is None:
            test_status = TestStatus.Pass
            test_note = 'Passed in %s seconds.' % child.attrib['time']
        else:
            test_status = TestStatus.Fail
            test_note = 'Failed'

        test_data[int(child.attrib['zephyr_tcid'])] = {'status': test_status,
                                                       'note': test_note}

 #   zm.update_test_status(tests, test_data)

    zm.logout()


class BulkAssigns:
    Creator, Anyone, Individual = range(1, 4)


class TestStatus:
    ChangeStatus, Pass, Fail, WIP, Blocked = range(0, 5)


class ZephyrManager:
    def __init__(self, username, password, urlWSDL):
        self.user_name = username
        self.password = password
        self.url = urlWSDL
        self.client = Client(self.url)
        self.session = None

    def login(self):
        self.session = self.client.service.login(self.user_name, self.password)
        # print 'Logged In.'
        # print 'The session token is: %s\n' % session

    def logout(self):
        self.client.service.logout(self.session)
        self.session = None

    def get_user_list(self):
        sc = self.client.factory.create('ns0:remoteCriteria')
        sc.searchName = ''
        sc.searchOperation = ''
        sc.searchValue = ''

        ru = self.client.service.getUsersByCriteria(sc, 'true', self.session)

        return ru

    def get_projects_list(self):
        sc = self.client.factory.create('ns0:remoteCriteria')
        sc.searchName = ''
        sc.searchOperation = ''
        sc.searchValue = ''

        rp = self.client.service.getProjectsByCriteria(sc, 'true', self.session)

        return rp

    def get_releases_for_project(self, project):
        releases = []

        sc = self.client.factory.create('ns0:remoteCriteria')
        sc.searchName = ''
        sc.searchOperation = ''
        sc.searchValue = ''

        rr = self.client.service.getReleasesByCriteria(sc, 'true', self.session)

        # Prints list length of RP
        # print 'Returned releases(s): %s' % len(rr)

        # Goes through all list entries and prints the name and startDate for each entry
        for key in rr:
            if key.remoteProjectData.remoteData.name == project:
                releases.append(key)
                # print 'name: %s' % rKey.name
                #print 'startDate: %s' % key.startDate

        return releases

    def create_test_execution(self, project, release, name, build, environment, start_date, end_date):
        ret = 0

        try:
            rel_id = -1

            releases = self.get_releases_for_project(project)

            for key in releases:
                if key.name == release:
                    rel_id = key.id

            if rel_id != -1:
                # print 'Creating new test cycle'
                cycle = self.client.factory.create('remoteCycle')

                cycle.name = name
                cycle.build = build
                cycle.environment = environment
                cycle.startDate = start_date
                cycle.endDate = end_date
                cycle.releaseId = rel_id

                # print cycle

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

    def get_test_case_tree(self, release_id, repo_folder):
        remote_criteria = []

        sc0 = self.client.factory.create('ns0:remoteCriteria')
        sc0.searchName = 'releaseId'
        sc0.searchOperation = 'EQUALS'
        sc0.searchValue = release_id

        sc1 = self.client.factory.create('ns0:remoteCriteria')
        sc1.searchName = 'name'
        sc1.searchOperation = 'EQUALS'
        sc1.searchValue = repo_folder

        remote_criteria.append(sc0)
        remote_criteria.append(sc1)

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


if __name__ == "__main__":
    main()