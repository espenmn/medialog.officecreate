# -*- coding: utf-8 -*-
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)

import medialog.officecreate


class MedialogOfficecreateLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=medialog.officecreate)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.officecreate:default')


MEDIALOG_OFFICECREATE_FIXTURE = MedialogOfficecreateLayer()


MEDIALOG_OFFICECREATE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_OFFICECREATE_FIXTURE,),
    name='MedialogOfficecreateLayer:IntegrationTesting',
)


MEDIALOG_OFFICECREATE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_OFFICECREATE_FIXTURE,),
    name='MedialogOfficecreateLayer:FunctionalTesting',
)
