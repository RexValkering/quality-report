"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

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

import unittest
import urllib.error

from hqlib.metric_source import Jira, JiraFilter


class JiraUnderTest(Jira):  # pylint: disable=too-few-public-methods
    """ Override class to return a fixed JSON file. """

    nr_query_results = 5
    view_url = 'http://jira/view'
    issues = '[]'

    def url_read(self, url):  # pylint: disable=unused-argument
        """ Return the static content. """
        if 'raise' in url:
            raise urllib.error.HTTPError(None, None, None, None, None)
        else:
            return '{{"searchUrl": "http://jira/search", "viewUrl": "{0}", "total": {1}, "issues": {2}}}'.format(
                self.view_url, self.nr_query_results, self.issues)


class JiraFilterTest(unittest.TestCase):
    """ Test the Jira filter metric source. """
    def test_nr_issues(self):
        """ Test that the number of items equals what Jira returns. """
        self.assertEqual(5, JiraFilter('', '', '', jira=JiraUnderTest('', '', '')).nr_issues('12345'))

    def test_nr_issues_on_error(self):
        """ Test that the number of items is -1 when an error occurs. """
        self.assertEqual(-1, JiraFilter('', '', '', jira=JiraUnderTest('raise', '', '')).nr_issues('12345'))

    def test_sum_field(self):
        """ Test that the number of points equals what Jira returns. """
        jira = JiraUnderTest('', '', '')
        jira.issues = '[{"fields": {"customfield_10002": "2"}},' \
                      ' {"fields": {"customfield_10002": 10}},' \
                      ' {"fields": {"customfield_10002": null}}]'
        self.assertEqual(12, JiraFilter('', '', '', jira=jira, field_name='customfield_10002').sum_field('12345'))

    def test_nr_issues_with_field_empty(self):
        """ Test that the number of issues with an empty field can be counted. """
        jira = JiraUnderTest('', '', '')
        jira.issues = '[{"fields": {"customfield_10002": "2"}},' \
                      ' {"fields": {"customfield_10002": 10}},' \
                      ' {"fields": {"customfield_10002": null}}]'
        self.assertEqual(1, JiraFilter('', '', '', jira=jira,
                                       field_name='customfield_10002').nr_issues_with_field_empty('12345'))

    def test_sum_fields_on_error(self):
        """ Test that the number of points is -1 when an error occurs. """
        self.assertEqual(-1, JiraFilter('', '', '', jira=JiraUnderTest('raise', '', '')).sum_field('12345'))

    def test_url(self):
        """ Test that the Jira filter returns the correct url for the filters. """
        self.assertEqual(['http://jira/view'],
                         JiraFilter('', '', '', jira=JiraUnderTest('http://jira/', '', '')).metric_source_urls('12345'))
