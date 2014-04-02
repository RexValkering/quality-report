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

import unittest
from qualitylib import metric, domain


class FakeBirt(object):
    ''' Provide for a fake Birt object. '''

    def __init__(self, test_design=True):
        self.__test_design = test_design

    def has_test_design(self, birt_id):  # pylint: disable=unused-argument
        return self.__test_design

    @staticmethod
    def approved_user_stories(birt_id):  # pylint: disable=unused-argument
        ''' Return the number of approved user stories. '''
        return 20

    @staticmethod
    def nr_user_stories(birt_id):  # pylint: disable=unused-argument
        ''' Return the total number of user stories. '''
        return 25

    @staticmethod
    def nr_user_stories_with_sufficient_ltcs(birt_id):  
        # pylint: disable=unused-argument, invalid-name
        ''' Return the number of user stories with enough logical test 
            cases. '''
        return 23

    @staticmethod
    def whats_missing_url(product):  # pylint: disable=unused-argument
        ''' Return the url for the what's missing report. '''
        return 'http://whats_missing'


class FakeSubject(object):
    ''' Provide for a fake subject. '''
    version = ''

    def __init__(self, birt_id=True):
        self.__birt_id = birt_id

    def birt_id(self):
        ''' Return the Birt id of the subject. '''
        return 'birt id' if self.__birt_id else ''

    def product_version(self):
        ''' Return the product version. '''
        return self.version


class ReviewedAndApprovedUserStoriesTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the ReviewedAndApprovedUserStories metric. '''
    def setUp(self):  # pylint: disable=invalid-name
        birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(birt=birt)
        self.__metric = metric.ReviewedAndApprovedUserStories( \
            subject=self.__subject, project=self.__project)

    def test_value(self):
        ''' Test that the value of the metric is the percentage of approved
            user stories as reported by Birt. '''
        self.assertEqual(80, self.__metric.value())

    def test_url(self):
        ''' Test the url is correct. '''
        self.assertEqual({'Birt': 'http://whats_missing'}, self.__metric.url())

    def test_can_be_measured(self):
        ''' Test that the metric can  be measured when the project has Birt and
            the product has a Birt id and is a trunk version. '''
        self.failUnless(metric.ReviewedAndApprovedUserStories.\
                        can_be_measured(self.__subject, self.__project))

    def test_cant_be_measured_without_birt(self):
        ''' Test that the metric can not be measured when the project has no
            Birt. '''
        self.failIf(metric.ReviewedAndApprovedUserStories.\
                    can_be_measured(self.__subject, domain.Project()))

    def test_cant_be_measured_without_birt_id(self):
        ''' Test that the metric can not be measured when the product has no
            Birt id. '''
        product = FakeSubject(birt_id=False)
        self.failIf(metric.ReviewedAndApprovedUserStories.\
                    can_be_measured(product, self.__project))

    def test_cant_be_measured_for_released_product(self):
        ''' Test that the metric can only be measured for trunk versions. '''
        product = self.__subject
        product.version = '1.1'
        self.failIf(metric.ReviewedAndApprovedUserStories.\
                    can_be_measured(product, self.__project))

    def test_cant_be_measured_without_test_design(self):
        ''' Test that the metric can not be measured if the product has no
            test design report in Birt. '''
        birt = FakeBirt(test_design=False)
        project = domain.Project(birt=birt)
        self.failIf(metric.ReviewedAndApprovedUserStories.\
                    can_be_measured(self.__subject, project))


class UserStoriesWithEnoughLTCsTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the user-stories-with-enough-logical-test-cases-
        metric. '''
    def setUp(self):  # pylint: disable=invalid-name
        self.__birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(birt=self.__birt)
        self.__metric = metric.UserStoriesWithEnoughLogicalTestCases( \
            subject=self.__subject, project=self.__project)

    def test_value(self):
        ''' Test that the value of the metric is the percentage of user stories 
            that has enough logical test cases as reported by Birt. '''
        self.assertEqual(100 * 23 / 25., self.__metric.value())

    def test_url(self):
        ''' Test the url is correct. '''
        self.assertEqual(dict(Birt=self.__birt.whats_missing_url('product')), 
                         self.__metric.url())

    def test_can_be_measured(self):
        ''' Test that the metric can  be measured when the project has Birt and
            the product has a Birt id and is a trunk version. '''
        self.failUnless(metric.UserStoriesWithEnoughLogicalTestCases.\
                        can_be_measured(self.__subject, self.__project))

    def test_cant_be_measured_without_birt(self):
        ''' Test that the metric can not be measured when the project has no
            Birt. '''
        self.failIf(metric.UserStoriesWithEnoughLogicalTestCases.\
                    can_be_measured(self.__subject, domain.Project()))

    def test_cant_be_measured_without_birt_id(self):
        ''' Test that the metric can not be measured when the product has no
            Birt id. '''
        product = FakeSubject(birt_id=False)
        self.failIf(metric.UserStoriesWithEnoughLogicalTestCases.\
                    can_be_measured(product, self.__project))

    def test_cant_be_measured_for_released_product(self):
        ''' Test that the metric can only be measured for trunk versions. '''
        product = self.__subject
        product.version = '1.1'
        self.failIf(metric.UserStoriesWithEnoughLogicalTestCases.\
                    can_be_measured(product, self.__project))
