# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from medialog.officecreate.testing import MEDIALOG_OFFICECREATE_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that medialog.officecreate is properly installed."""

    layer = MEDIALOG_OFFICECREATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if medialog.officecreate is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'medialog.officecreate'))

    def test_browserlayer(self):
        """Test that IMedialogOfficecreateLayer is registered."""
        from medialog.officecreate.interfaces import (
            IMedialogOfficecreateLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IMedialogOfficecreateLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MEDIALOG_OFFICECREATE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('medialog.officecreate')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if medialog.officecreate is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'medialog.officecreate'))

    def test_browserlayer_removed(self):
        """Test that IMedialogOfficecreateLayer is removed."""
        from medialog.officecreate.interfaces import \
            IMedialogOfficecreateLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMedialogOfficecreateLayer, utils.registered_layers())
