# -*- coding: utf-8 -*-
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class TemplateIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_template_schema(self):
        fti = queryUtility(IDexterityFTI, name='Template')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Template')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_template_fti(self):
        fti = queryUtility(IDexterityFTI, name='Template')
        self.assertTrue(fti)

    def test_ct_template_factory(self):
        fti = queryUtility(IDexterityFTI, name='Template')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_template_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Template',
            id='template',
        )


        parent = obj.__parent__
        self.assertIn('template', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('template', parent.objectIds())

    def test_ct_template_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Template')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
