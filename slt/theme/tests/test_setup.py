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
        from slt.theme.browser.interfaces import ISltThemeLayer
        from plone.browserlayer import utils
        self.assertIn(ISltThemeLayer, utils.registered_layers())

    def get_css_resource(self, name):
        return getToolByName(self.portal, 'portal_css').getResource(name)

    def test_cssregistry__main__title(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertIsNone(resource.getTitle())

    def test_cssregistry__main__authenticated(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertFalse(resource.getAuthenticated())

    def test_cssregistry__main__compression(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertEqual(resource.getCompression(), 'safe')

    def test_cssregistry__main__conditionalcomment(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertEqual(resource.getConditionalcomment(), '')

    def test_cssregistry__main__cookable(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertTrue(resource.getCookable())

    def test_cssregistry__main__enabled(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertTrue(resource.getEnabled())

    def test_cssregistry__main__expression(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertEqual(resource.getExpression(), 'request/HTTP_X_THEME_ENABLED | nothing')

    def test_cssregistry__main__media(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertIsNone(resource.getMedia())

    def test_cssregistry__main__rel(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertEqual(resource.getRel(), 'stylesheet')

    def test_cssregistry__main__rendering(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertEqual(resource.getRendering(), 'link')

    def test_cssregistry__main__applyPrefix(self):
        resource = self.get_css_resource('++theme++slt.theme/css/main.css')
        self.assertTrue(resource.getApplyPrefix())

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-slt.theme:default'), u'0')

    def test_metadata__installed__plone_app_theming(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.app.theming'))

    def get_theme(self):
        from plone.app.theming.interfaces import IThemeSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        return getUtility(IRegistry).forInterface(IThemeSettings)

    def test_them__currentTheme(self):
        theme = self.get_theme()
        self.assertEqual(theme.currentTheme, u'slt.theme')

    def test_theme__doctype(self):
        theme = self.get_theme()
        self.assertEqual(theme.doctype, '<!DOCTYPE html>')

    def test_theme__enabled(self):
        theme = self.get_theme()
        self.assertTrue(theme.enabled)

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
        from slt.theme.browser.interfaces import ISltThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(ISltThemeLayer, utils.registered_layers())

    def test_uninstall__cssregistry_main(self):
        self.uninstall_package()
        resources = set(getToolByName(self.portal, 'portal_css').getResourceIds())
        self.assertNotIn('++theme++slt.theme/css/main.css', resources)

    def test_uninstall__metadata__installed__plone_app_theming(self):
        self.uninstall_package()
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.app.theming'))

    def test_uninstall__them__currentTheme(self):
        theme = self.get_theme()
        self.assertEqual(theme.currentTheme, u'slt.theme')

    def test_unintall__theme__enabled(self):
        theme = self.get_theme()
        self.assertTrue(theme.enabled)
