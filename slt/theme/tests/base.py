from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import unittest


class SltThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import slt.theme
        self.loadZCML(package=slt.theme)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'slt.theme:default')

    def tearDownZope(self, app):
        """Tear down Zope."""


FIXTURE = SltThemeLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="SltThemeLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="SltThemeLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
