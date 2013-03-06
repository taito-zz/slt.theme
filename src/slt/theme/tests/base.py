from Testing import ZopeTestCase as ztc
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.utils import createContentInContainer
from plone.testing import z2
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import directlyProvides
from zope.lifecycleevent import modified
from zope.publisher.browser import TestRequest

import mock
import unittest


class SltThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Required by Products.CMFPlone:plone-content to setup defaul plone site.
        z2.installProduct(app, 'Products.PythonScripts')
        z2.installProduct(app, 'Products.ATCountryWidget')

        # Load ZCML
        import collective.cart.shopping
        self.loadZCML(package=collective.cart.shopping)
        z2.installProduct(app, 'collective.cart.shopping')
        z2.installProduct(app, 'collective.cart.shipping')

        # Load ZCML
        import slt.theme
        self.loadZCML(package=slt.theme)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup

        self.applyProfile(portal, 'slt.theme:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.cart.shipping')
        z2.uninstallProduct(app, 'collective.cart.shopping')
        z2.uninstallProduct(app, 'Products.ATCountryWidget')
        z2.uninstallProduct(app, 'Products.PythonScripts')


FIXTURE = SltThemeLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="SltThemeLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="SltThemeLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        ztc.utils.setupCoreSessions(self.layer['app'])
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def create_content(self, ctype, parent=None, **kwargs):
        if parent is None:
            parent = self.portal
        content = createContentInContainer(parent, ctype, checkConstraints=False, **kwargs)
        modified(content)
        return content

    def create_view(self, view, context=None):
        if context is None:
            context = self.portal
        request = TestRequest()
        directlyProvides(request, IAttributeAnnotatable)
        request.set = mock.Mock()
        return view(context, request)


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
