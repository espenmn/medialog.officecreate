# -*- coding: utf-8 -*-
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_FUNCTIONAL_TESTING
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_INTEGRATION_TESTING
from medialog.officecreate.views.p_p_merge_view import IPPMergeView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_p_p_merge_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='p-p-merge-view'
        )
        self.assertTrue(IPPMergeView.providedBy(view))

    def test_p_p_merge_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='p-p-merge-view'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IPPMergeView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
