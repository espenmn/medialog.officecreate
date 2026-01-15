# -*- coding: utf-8 -*-
from medialog.officecreate.behaviors.subject_mover import ISubjectMoverMarker
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class SubjectMoverIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_subject_mover(self):
        behavior = getUtility(IBehavior, 'medialog.officecreate.subject_mover')
        self.assertEqual(
            behavior.marker,
            ISubjectMoverMarker,
        )
