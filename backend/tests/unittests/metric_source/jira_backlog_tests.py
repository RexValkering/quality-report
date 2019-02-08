"""
Copyright 2012-2018 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import unittest
from unittest.mock import patch
from hqlib.metric_source import JiraFilter
from hqlib.metric_source.jira_backlog import JiraBacklog


@patch.object(JiraFilter, 'nr_issues')
class JiraBacklogTests(unittest.TestCase):
    """ Unit tests of the constructor of the Jira class. """

    @patch.object(JiraFilter, '__init__')
    def test_init(self, mock_init, mock_nr_issues):
        """ Tests that the inner JiraFilter is initialized with correct parameters """
        mock_init.return_value = None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        backlog.nr_user_stories()
        mock_nr_issues.assert_called_once()
        mock_init.assert_called_once_with('url!', 'username!', 'password!')
        self.assertEqual('Jira backlog', backlog.metric_source_name)

    def test_nr_user_stories(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.nr_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('project = "project!" AND type = Story')

    def test_nr_user_stories_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"nr_user_stories": ['1st {project}', '2nd {project}']})
        result = backlog.nr_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_nr_user_stories_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"nr_user_stories": [11, '12']})
        result = backlog.nr_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_approved_user_stories(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.approved_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_approved_user_stories_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"approved_user_stories": ['1st {project}', '2nd {project}']})
        result = backlog.approved_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_approved_user_stories_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"approved_user_stories": [11, '12']})
        result = backlog.approved_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_reviewed_user_stories(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.reviewed_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_reviewed_user_stories_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"reviewed_user_stories": ['1st {project}', '2nd {project}']})
        result = backlog.reviewed_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_reviewed_user_stories_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"reviewed_user_stories": [11, '12']})
        result = backlog.reviewed_user_stories()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_nr_user_stories_with_sufficient_ltcs(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.nr_user_stories_with_sufficient_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_nr_user_stories_with_sufficient_ltcs_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"nr_user_stories_with_sufficient_ltcs": ['1st {project}', '2nd {project}']})
        result = backlog.nr_user_stories_with_sufficient_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_nr_user_stories_with_sufficient_ltcs_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog(
            'url!', 'username!', 'password!', 'whatever!?', {"nr_user_stories_with_sufficient_ltcs": [11, '12']})
        result = backlog.nr_user_stories_with_sufficient_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_reviewed_ltcs(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.reviewed_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_reviewed_ltcs_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"reviewed_ltcs": ['1st {project}', '2nd {project}']})
        result = backlog.reviewed_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_reviewed_ltcs_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"reviewed_ltcs": [11, '12']})
        result = backlog.reviewed_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_nr_ltcs(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.nr_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_nr_ltcs_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"nr_ltcs": ['1st {project}', '2nd {project}']})
        result = backlog.nr_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_nr_ltcs_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"nr_ltcs": [11, '12']})
        result = backlog.nr_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_approved_ltcs(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.approved_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_approved_ltcs_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"approved_ltcs": ['1st {project}', '2nd {project}']})
        result = backlog.approved_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_approved_ltcs_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"approved_ltcs": [11, '12']})
        result = backlog.approved_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_nr_automated_ltcs(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.nr_automated_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_nr_automated_ltcs_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"nr_automated_ltcs": ['1st {project}', '2nd {project}']})
        result = backlog.nr_automated_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_nr_automated_ltcs_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"nr_automated_ltcs": [11, '12']})
        result = backlog.nr_automated_ltcs()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_nr_ltcs_to_be_automated(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.nr_ltcs_to_be_automated()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_nr_ltcs_to_be_automated_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"nr_ltcs_to_be_automated": ['1st {project}', '2nd {project}']})
        result = backlog.nr_ltcs_to_be_automated()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_nr_ltcs_to_be_automated_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"nr_ltcs_to_be_automated": [11, '12']})
        result = backlog.nr_ltcs_to_be_automated()
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    def test_nr_manual_ltcs_too_old(self, mock_nr_issues):
        """ Tests that the function invokes correct default jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!')
        result = backlog.nr_manual_ltcs_too_old('1', 1)
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once()

    def test_nr_manual_ltcs_too_old_custom(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jql query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'project!',
                              {"nr_manual_ltcs_too_old": ['1st {project}', '2nd {project}']})
        result = backlog.nr_manual_ltcs_too_old('1', 1)
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('1st project!', '2nd project!')

    def test_nr_manual_ltcs_too_old_custom_filter_number(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = 1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?', {"nr_manual_ltcs_too_old": [11, '12']})
        result = backlog.nr_manual_ltcs_too_old('1', 1)
        self.assertEqual(1, result)
        mock_nr_issues.assert_called_once_with('11', '12')

    # placeholder tests

    def test_nr_manual_ltcs(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = -1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?')
        result = backlog.nr_manual_ltcs()
        self.assertEqual(-1, result)

    def test_date_of_last_manual_test(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = -1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?')
        result = backlog.date_of_last_manual_test()
        self.assertEqual(datetime.datetime.min, result)

    def test_manual_test_execution_url(self, mock_nr_issues):
        """ Tests that the function invokes correct custom jira filter number instead of the query. """
        mock_nr_issues.return_value = -1, None
        backlog = JiraBacklog('url!', 'username!', 'password!', 'whatever!?')
        result = backlog.manual_test_execution_url()
        self.assertEqual('dull!', result)
