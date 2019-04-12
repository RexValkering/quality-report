"""
Copyright 2012-2018 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file exceppt in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import logging
import datetime
from typing import List

from hqlib.typing import DateTime
from .abstract.backlog import Backlog

JQL_CONFIG = {
    "nr_user_stories": 'project = "{project}" AND type = Story',
    "approved_user_stories": 'project = "{project}" AND type = Story AND '
                             '"Ready status" = "<font color = \"#888720\"><b>Approved</b></font>"',
    "reviewed_user_stories": 'project = "{project}" AND type = Story AND "Ready status" is not EMPTY',

    "nr_user_stories_with_sufficient_ltcs":
        'project = "{project}" AND type = Story AND issueFunction in hasLinks("is tested by") '
        'AND "Expected number of LTC\'s" > 0',

    "ltcs_for_user_story": 'project = "{project}" AND type = "Logical Test Case" '
                           'AND issue in linkedIssues({story-id}, "is tested by")',

    "reviewed_ltcs": 'project = "{project}" AND type = "Logical Test Case" AND "Review comments" is not EMPTY',

    "nr_ltcs": 'project = "{project}" AND type = "Logical Test Case"',
    "approved_ltcs": 'project = "{project}" AND type = "Logical Test Case" AND Approved = Yes',

    "nr_automated_ltcs": 'project = "{project}" AND type = "Logical Test Case" AND '
                         '"Test execution" = "Automated" AND status != open',
    "nr_ltcs_to_be_automated": 'project = "{project}" AND type = "Logical Test Case" AND '
                               '"Test execution" = "Automated" AND status = open',
    "nr_manual_ltcs": 'project = "{project}" AND type = "Logical Test Case" AND "Test execution" = Manual',
    "date_of_last_manual_test": '',
    "manual_test_execution_url": '',
    "nr_manual_ltcs_too_old": ''
}


class JiraBacklog(Backlog):
    """ Class representing the Backlog using Jira jql filters. """

    metric_source_name = 'Jira backlog'

    # pylint: disable=too-many-arguments
    def __init__(self, url: str, username: str, password: str, project: str, expected_ltcs_field: str=None,
                 jql_config=JQL_CONFIG) -> None:
        self._url = url
        self._username = username
        self._expected_ltcs_field = expected_ltcs_field
        self._password = password
        self._project = project
        self._jql_config = jql_config
        super().__init__(url=url)

    def _number_of_issues_in_jql(self, *jql: str):
        from ..metric_source import JiraFilter
        return JiraFilter(self._url, self._username, self._password).nr_issues(*jql)

    def nr_user_stories(self) -> int:
        """ Return the total number of user stories. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['nr_user_stories']))[0]

    def __format_jql_list(self, jql, param2: str = None) -> List[str]:
        return [str(jql).format(param2, project=self._project)] \
            if not isinstance(jql, list) else [str(j).format(param2, project=self._project) for j in jql]

    def approved_user_stories(self) -> int:
        """ Return the number of user stories that have been approved. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['approved_user_stories']))[0]

    def reviewed_user_stories(self) -> int:
        """ Return the number of user stories that have been reviewed. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['reviewed_user_stories']))[0]

    def nr_user_stories_with_sufficient_ltcs(self) -> int:
        """ Return the number of user stories that have enough logical test cases. """

        from ..metric_source import Jira
        jira = Jira(self._url, self._username, self._password)

        expected_ltcs_field_id = jira.get_field_id(self._expected_ltcs_field)
        if expected_ltcs_field_id is None:
            return -1

        try:
            stories = []
            jql_list = self.__format_jql_list(self._jql_config['nr_user_stories_with_sufficient_ltcs'])
            for jql in jql_list:
                stories += jira.get_query(jql)['issues']

            ret = []
            for story in stories:
                if len(story['fields']['issuelinks']) >= story['fields'][expected_ltcs_field_id]:
                    ret.append(story)
            return len(ret)
        except KeyError as reason:
            logging.error('Error processing jira response. The key %s not found!', reason)
            return -1

    def reviewed_ltcs(self) -> int:
        """ Return the number of reviewed logical test cases for the product. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['reviewed_ltcs']))[0]

    def nr_ltcs(self) -> int:
        """ Return the number of logical test cases. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['nr_ltcs']))[0]

    def approved_ltcs(self) -> int:
        """ Return the number of approved logical test casess. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['approved_ltcs']))[0]

    def nr_automated_ltcs(self) -> int:
        """ Return the number of logical test cases that have been implemented as automated tests. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['nr_automated_ltcs']))[0]

    def nr_ltcs_to_be_automated(self) -> int:
        """ Return the number of logical test cases for the product that have to be automated. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['nr_ltcs_to_be_automated']))[0]

    def nr_manual_ltcs(self, version: str = 'trunk') -> int:
        """ Return the number of logical test cases for the product that are executed manually. """
        return -1

    def date_of_last_manual_test(self, version: str = 'trunk') -> DateTime:
        """ Return the date when the product/version was last tested manually. """
        return datetime.datetime.min

    def manual_test_execution_url(self, version: str = 'trunk') -> str:
        """ Return the url for the manual test execution report. """
        return 'dull!'

    def nr_manual_ltcs_too_old(self, version: str, target: int) -> int:
        """ Return the number of manual logical test cases that have not been executed for target amount of days. """
        return self._number_of_issues_in_jql(*self.__format_jql_list(self._jql_config['nr_manual_ltcs_too_old']))[0]
