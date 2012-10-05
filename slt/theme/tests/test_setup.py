from Products.CMFCore.utils import getToolByName
from slt.theme.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('slt.theme'))

    def test_browserlayer(self):
        from slt.theme.browser.interfaces import ISltPolicyLayer
        from plone.browserlayer import utils
        self.assertIn(ISltPolicyLayer, utils.registered_layers())

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-slt.theme:default'), u'0')

    def test_metadata__installed__plone_app_theming(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.app.theming'))

    def uninstall_package(self):
        """Uninstall package: slt.theme."""
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['slt.theme'])

    def test_uninstall__package(self):
        self.uninstall_package()
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertFalse(installer.isProductInstalled('slt.theme'))

    def test_uninstall__browserlayer(self):
        self.uninstall_package()
        from slt.theme.browser.interfaces import ISltPolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(ISltPolicyLayer, utils.registered_layers())

    def test_uninstall__metadata__installed__plone_app_theming(self):
        self.uninstall_package()
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.app.theming'))
