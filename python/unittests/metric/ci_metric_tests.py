'''
Copyright 2012-2014 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from qualitylib import metric, domain
import unittest


class FakeJenkins(object):
    ''' Fake Jenkins instance for testing purposes. '''
    # pylint: disable=unused-argument

    UNSTABLE_ARTS_URL = {}

    @classmethod
    def failing_jobs_url(cls, *args):
        ''' Return the url(s) of the failing job(s). '''
        return {'job_name (3 dagen)': 'http://jenkins/job_name'}

    @staticmethod
    def number_of_jobs(*args):
        ''' Return the total number of CI jobs. '''
        return 2

    @staticmethod
    def number_of_assigned_jobs():
        ''' Return the number of jobs assigned to a team. '''
        return 2

    @classmethod
    def unstable_arts_url(cls, *args, **kwargs):
        ''' Return the urls for the unstable ARTs. '''
        return cls.UNSTABLE_ARTS_URL

    @staticmethod
    def unassigned_jobs_url():
        ''' Return the urls for the unassigned jobs. '''
        return dict(job='http://job')

    @classmethod
    def unused_jobs_url(cls, *args):
        ''' Return the url(s) of the unused job(s). '''
        return {'job_name (300 dagen)': 'http://jenkins/job_name'}


class FailingCIJobsCommonTestsMixin(object):
    ''' Unit tests of the failing CI jobs metric that don't depend on whether
        the metric is reporting on a specific team or not. '''

    def test_value(self):
        ''' Test that the value equals the number of failing jobs. '''
        self.assertEqual(1, self._metric.value())

    def test_url(self):
        ''' Test that the url of the metric equals the url of Jenkins. '''
        self.assertEqual(FakeJenkins().failing_jobs_url(), self._metric.url())

    def test_report(self):
        ''' Test the metric report. '''
        self.assertEqual(self.expected_report, self._metric.report())

    def test_label(self):
        ''' Test that the label to use in the HTML report is correct. '''
        self.assertEqual('Falende jobs', self._metric.url_label())


class ProjectFailingCIJobsTest(FailingCIJobsCommonTestsMixin, 
                               unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the failing CI jobs metric without a specific team. '''

    expected_report = '1 van de 2 CI-jobs faalt.'

    def setUp(self):  # pylint: disable=invalid-name
        ''' Create the text fixture. '''
        self._subject = None
        self._project = domain.Project(build_server=FakeJenkins())
        self._metric = metric.ProjectFailingCIJobs(subject=self._subject,
                                                   project=self._project)

    def test_can_be_measured(self):
        ''' Test that the metric can be measured if there is a build server. '''
        self.failUnless(metric.ProjectFailingCIJobs.\
                        can_be_measured(self._project, self._project))

    def test_cant_be_measured_without_build_server(self):
        ''' Test that the metric cannot be measured without build server. '''
        project = domain.Project()
        for index in range(2):
            team = domain.Team('Team %d' % index)
            project.add_team(team, responsible=True)
        self.failIf(metric.ProjectFailingCIJobs.can_be_measured(team, project))


class TeamFailingCIJobsTest(FailingCIJobsCommonTestsMixin, unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the failing CI jobs metric with a specific team. '''

    expected_report = '1 van de 2 CI-jobs waarvoor team ' \
                      'Team verantwoordelijk is faalt.'

    def setUp(self):  # pylint: disable=invalid-name
        ''' Create the text fixture. '''
        self._project = domain.Project(build_server=FakeJenkins())
        self._subject = domain.Team('Team')
        self._project.add_team(self._subject, responsible=True)
        self._project.add_team(domain.Team('Another team'), responsible=True)
        self._metric = metric.TeamFailingCIJobs(subject=self._subject, 
                                                project=self._project)

    def test_can_be_measured(self):
        ''' Test that the metric can be measured when the project has 
            multiple teams. '''
        self.failUnless(metric.TeamFailingCIJobs.can_be_measured(self._subject, 
                                                                 self._project))

    def test_wont_be_measured_unless_multiple_teams(self):
        ''' Test that the metric won't be measured unless the project has 
            multiple teams. '''
        project = domain.Project(build_server=FakeJenkins())
        team = domain.Team('Single team')
        project.add_team(team, responsible=True)
        self.failIf(metric.TeamFailingCIJobs.can_be_measured(team, project))

    def test_cant_be_measured_without_build_server(self):
        ''' Test that the metric cannot be measured without build server. '''
        project = domain.Project()
        for index in range(2):
            team = domain.Team('Team %d' % index)
            project.add_team(team, responsible=True)
        self.failIf(metric.TeamFailingCIJobs.can_be_measured(team, project))


class UnusedCIJobsCommonTestsMixin(object):
    ''' Unit tests for the unused CI jobs metric that don't depend on whether
        the metric is reporting on a specific team or not. '''

    def test_value(self):
        ''' Test that the value equals the number of failing jobs. '''
        self.assertEqual(1, self._metric.value())

    def test_url(self):
        ''' Test that the url of the metric equals the url of Jenkins. '''
        self.assertEqual(FakeJenkins().unused_jobs_url(), self._metric.url())

    def test_report(self):
        ''' Test the metric report. '''
        self.assertEqual(self.expected_report, self._metric.report())

    def test_label(self):
        ''' Test that the label to use in the HTML report is correct. '''
        self.assertEqual('Ongebruikte jobs', self._metric.url_label())


class TeamUnusedCIJobsTest(UnusedCIJobsCommonTestsMixin, unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the unused CI jobs metric with a specific team. '''

    expected_report = '1 van de 2 CI-jobs waarvoor team ' \
                      'Team verantwoordelijk is is ongebruikt.'

    def setUp(self):  # pylint: disable=invalid-name
        ''' Create the text fixture. '''
        self._project = domain.Project(build_server=FakeJenkins())
        self.__team = domain.Team('Team')
        self._project.add_team(self.__team)
        self._project.add_team(domain.Team('Another team'))
        self._metric = metric.TeamUnusedCIJobs(subject=self.__team,
                                               project=self._project)

    def test_can_be_measured(self):
        ''' Test that the metric can be measured when the project as multiple
            teams. '''
        self.failUnless(metric.TeamUnusedCIJobs.can_be_measured(self.__team,
                                                                self._project))

    def test_wont_be_measured_unless_multiple_teams(self):
        ''' Test that the metric won't be measured unless the project has
            multiple teams. '''
        project = domain.Project(build_server=FakeJenkins())
        project.add_team(self.__team)
        self.failIf(metric.TeamUnusedCIJobs.can_be_measured(self.__team, 
                                                            project))

    def test_cant_be_measured_without_build_server(self):
        ''' Test that the metric cannot be measured without build server. '''
        project = domain.Project()
        project.add_team(self.__team)
        project.add_team(domain.Team('Another team'))
        self.failIf(metric.TeamUnusedCIJobs.can_be_measured(self.__team, 
                                                            project))


class ProjectUnusedCIJobs(UnusedCIJobsCommonTestsMixin, unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the unused CI jobs metric without a specific team. '''

    expected_report = '1 van de 2 CI-jobs is ongebruikt.'

    def setUp(self):  # pylint: disable=invalid-name
        ''' Create the text fixture. '''
        self._project = domain.Project(build_server=FakeJenkins())
        self._metric = metric.ProjectUnusedCIJobs(subject=self._project,
                                                  project=self._project)

    def test_can_be_measured(self):
        ''' Test that the metric can be measured if there is a build server. '''
        self.failUnless(metric.ProjectUnusedCIJobs.\
                        can_be_measured(self._project, self._project))

    def test_cant_be_measured_without_build_server(self):
        ''' Test that the metric cannot be measured without build server. '''
        project = domain.Project()
        self.failIf(metric.ProjectUnusedCIJobs.can_be_measured(project, 
                                                               project))


class ARTStabilityTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the ARTstability metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        project = domain.Project(build_server=FakeJenkins())
        self.__metric = metric.ARTStability(subject=domain.Street('a', 'b'), 
                                            project=project)

    def test_value_stable(self):
        ''' Test that the value of the metric equals the list of unstable ARTs
            return by Jenkins. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {}
        self.assertEqual(0, self.__metric.value())

    def test_report_stable(self):
        ''' Test that the report is correct. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {}
        self.assertEqual('Alle ARTs hebben de afgelopen 3 dagen succesvol ' \
                         'gedraaid in de "a"-straat.', self.__metric.report())

    def test_value_unstable(self):
        ''' Test that the value of the metric equals the list of unstable ARTs
            return by Jenkins. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {'unstable_art': 'http://url'}
        self.assertEqual(1, self.__metric.value())

    def test_report_unstable(self):
        ''' Test that the report is correct. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {'unstable_art': 'http://url'}
        self.assertEqual('1 ARTs hebben de afgelopen 3 dagen ' \
                         'niet succesvol gedraaid in de "a"-straat.', 
                         self.__metric.report())

    def test_url(self):
        ''' Test that the url equals the URL provided by Jenkins. '''
        self.assertEqual(FakeJenkins.unstable_arts_url(), self.__metric.url())

    def test_numerical_value(self):
        ''' Test that the numerical value is the number of unstable ARTs. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {'unstable_art': 'http://url'}
        self.assertEqual(1, self.__metric.numerical_value())

    def test_status_stable(self):
        ''' Test that the status is green when the number of unstable 
            ARTs is zero. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {}
        self.assertEqual('perfect', self.__metric.status())

    def test_status_unstable(self):
        ''' Test that the status is red when the number of unstable ARTs is
            not zero. '''
        FakeJenkins.UNSTABLE_ARTS_URL = {'unstable_art': 'http://url', 
                                         'unstable_art2': 'http://url'}
        self.assertEqual('red', self.__metric.status())


class FakeNagios(object):
    ''' Fake Nagios for testing purposes. '''
    @staticmethod
    def number_of_servers_sufficiently_available():  
        # pylint: disable=invalid-name
        ''' Fake the number of available servers. '''
        return 10

    @staticmethod
    def number_of_servers():
        ''' Fake the number of servers. '''
        return 12

    @staticmethod
    def number_of_servers_per_group():
        ''' Fake the server groups. '''
        return dict(group1=4, group2=8)

    @staticmethod
    def availability_url():
        ''' Fake the Nagios url. '''
        return 'http://nagios'


class ServerAvailabilityTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the server availability metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__project = domain.Project(nagios=FakeNagios())
        self.__team = domain.Team('Support team', is_support_team=True)
        self.__metric = metric.ServerAvailability(subject=self.__team, 
                                                  project=self.__project)

    def test_value(self):
        ''' Test that the availability is reported correctly. '''
        self.assertEqual(83., self.__metric.value())

    def test_report(self):
        ''' Test that the report is correct. '''
        self.assertEqual('Servers met voldoende beschikbaarheid is 83% ' \
                         '(10 van 12). Aantal servers per groep: group1: 4, ' \
                         'group2: 8.', self.__metric.report())

    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual(dict(Nagios='http://nagios'), self.__metric.url())

    def test_can_be_measured(self):
        ''' Test that the metric can be measured for support teams if Nagios
            is available. '''
        self.failUnless(metric.ServerAvailability.\
                        can_be_measured(self.__team, self.__project))

    def test_cant_be_measured_for_scrum_teams(self):
        ''' Test that the metric can only be measured for support teams. '''
        team = domain.Team('Scrum team', is_scrum_team=True)
        self.failIf(metric.ServerAvailability.can_be_measured(team,
                                                              self.__project))

    def test_cant_be_measured_without_nagios(self):
        ''' Test that the metric can not be measured without Nagios. '''
        project = domain.Project()
        self.failIf(metric.ServerAvailability.can_be_measured(self.__team,
                                                              project))


class AssignedCIJobsTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the assigned CI jobs metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__project = domain.Project(build_server=FakeJenkins())
        self.__project.add_team('team1')
        self.__project.add_team('team2')
        self.__metric = metric.AssignedCIJobs(subject=domain.Team('Team'), 
                                              project=self.__project)

    def test_value(self):
        ''' Test that the availability is reported correctly. '''
        self.assertEqual(100., self.__metric.value())

    def test_report(self):
        ''' Test that the report is correct. '''
        self.assertEqual('100% (2 van 2) van de CI-jobs is toegewezen aan ' \
                         'een team.', self.__metric.report())

    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual(FakeJenkins().unassigned_jobs_url(), 
                         self.__metric.url())

    def test_label(self):
        ''' Test that the label is correct. '''
        self.assertEqual('Niet toegewezen jobs', self.__metric.url_label())

    def test_can_be_measured(self):
        ''' Test that the metric can be measured when the project has a build 
            server and the project has more than one team. '''
        self.failUnless(metric.AssignedCIJobs.can_be_measured(self.__project, 
                                                              self.__project))

    def test_cant_be_measured_without_build_server(self):
        ''' Test that the metric can be measured when the project has a build 
            server and the project has more than one team. '''
        project = domain.Project()
        self.failIf(metric.AssignedCIJobs.can_be_measured(self.__project, 
                                                          project))

    def test_cant_be_measured_without_multiple_teams(self):
        ''' Test that the metric can be measured when the project has a build 
            server and the project has more than one team. '''
        project = domain.Project(build_server=FakeJenkins())
        self.failIf(metric.AssignedCIJobs.can_be_measured(project, project))
