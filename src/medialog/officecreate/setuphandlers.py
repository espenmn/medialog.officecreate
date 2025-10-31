# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "medialog.officecreate:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["medialog.officecreate.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    
    portal = api.portal.get()
    if not portal.get('templates', False):
        templates_folder = api.content.create(
            type='Folder',
            container=portal,
            id='templates',
            title='Templates',
        )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
