# -*- coding: utf-8 -*-
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_FUNCTIONAL_TESTING
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_INTEGRATION_TESTING
from medialog.officecreate.views.office_doc_view import IOfficeDocView
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
        api.content.create(self.portal, 'DocxExample', 'docx-example')
        

    def test_office_doc_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['docx-example'], self.portal.REQUEST),
            name='office-doc-view'
        )
        self.assertTrue(IOfficeDocView.providedBy(view))

    def test_office_doc_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='office-doc-view'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IOfficeDocView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
