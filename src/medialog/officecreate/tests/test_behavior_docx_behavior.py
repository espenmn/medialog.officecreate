# -*- coding: utf-8 -*-
from medialog.officecreate.behaviors.docx_behavior import IDocxBehaviorMarker
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class DocxBehaviorIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_docx_behavior(self):
        behavior = getUtility(IBehavior, 'medialog.officecreate.docx_behavior')
        self.assertEqual(
            behavior.marker,
            IDocxBehaviorMarker,
        )
