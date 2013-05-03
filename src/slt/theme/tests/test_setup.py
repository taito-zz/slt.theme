from Products.CMFCore.utils import getToolByName
from abita.utils.utils import get_roles
from slt.theme.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('slt.theme'))

    def get_action(self, name):
        """Get action.

        :param name: Name of action.
        :param type: str

        :rtype: action
        """
        return getattr(getattr(getToolByName(
            self.portal, 'portal_actions'), 'object_buttons'), name, None)

    def test_actions__object_buttons__feed_to_shop_top__i18n_domain(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(action.i18n_domain, 'slt.theme')

    def test_actions__object_buttons__feed_to_shop_top__meta_type(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(action.meta_type, 'CMF Action')

    def test_actions__object_buttons__feed_to_shop_top__title(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(action.title, 'Feed to Shop Top')

    def test_actions__object_buttons__feed_to_shop_top__description(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(action.description, '')

    def test_actions__object_buttons__feed_to_shop_top__url_expr(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(
            action.url_expr, 'string:${globals_view/getCurrentObjectUrl}/@@feed-to-shop-top')

    def test_actions__object_buttons__feed_to_shop_top__available_expr(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(
            action.available_expr, 'python: object.restrictedTraverse("feedable-to-shop-top")()')

    def test_actions__object_buttons__feed_to_shop_top__permissions(self):
        action = self.get_action('feed_to_shop_top')
        self.assertEqual(action.permissions, ('slt.theme: Manage feed for shop top',))

    def test_actions__object_buttons__feed_to_shop_top__visible(self):
        action = self.get_action('feed_to_shop_top')
        self.assertTrue(action.visible)

    def test_actions__object_buttons__unfeed_from_shop_top__i18n_domain(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(action.i18n_domain, 'slt.theme')

    def test_actions__object_buttons__unfeed_from_shop_top__meta_type(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(action.meta_type, 'CMF Action')

    def test_actions__object_buttons__unfeed_from_shop_top__title(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(action.title, 'Unfeed from Shop Top')

    def test_actions__object_buttons__unfeed_from_shop_top__description(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(action.description, '')

    def test_actions__object_buttons__unfeed_from_shop_top__url_expr(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(
            action.url_expr, 'string:${globals_view/getCurrentObjectUrl}/@@unfeed-from-shop-top')

    def test_actions__object_buttons__unfeed_from_shop_top__available_expr(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(
            action.available_expr, 'python: object.restrictedTraverse("unfeedable-from-shop-top")()')

    def test_actions__object_buttons__unfeed_from_shop_top__permissions(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertEqual(action.permissions, ('slt.theme: Manage feed for shop top',))

    def test_actions__object_buttons__unfeed_from_shop_top__visible(self):
        action = self.get_action('unfeed_from_shop_top')
        self.assertTrue(action.visible)

    def test_browserlayer(self):
        from slt.theme.browser.interfaces import ISltThemeLayer
        from plone.browserlayer import utils
        self.assertIn(ISltThemeLayer, utils.registered_layers())

    def test_memberdata_properties(self):
        memberdata = getToolByName(self.portal, 'portal_memberdata')
        ids = ['registration_number', ]
        for pid in ids:
            self.assertTrue(memberdata.hasProperty(pid))

    def get_css_resource(self, name):
        return getToolByName(self.portal, 'portal_css').getResource(name)

    def test_cssregistry__main__title(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertIsNone(resource.getTitle())

    def test_cssregistry__main__authenticated(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertFalse(resource.getAuthenticated())

    def test_cssregistry__main__compression(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertEqual(resource.getCompression(), 'safe')

    def test_cssregistry__main__conditionalcomment(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertEqual(resource.getConditionalcomment(), '')

    def test_cssregistry__main__cookable(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertTrue(resource.getCookable())

    def test_cssregistry__main__enabled(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertTrue(resource.getEnabled())

    def test_cssregistry__main__expression(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertEqual(resource.getExpression(), '')

    def test_cssregistry__main__media(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertIsNone(resource.getMedia())

    def test_cssregistry__main__rel(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertEqual(resource.getRel(), 'stylesheet')

    def test_cssregistry__main__rendering(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertEqual(resource.getRendering(), 'link')

    def test_cssregistry__main__applyPrefix(self):
        resource = self.get_css_resource('++resource++slt.theme/css/main.css')
        self.assertTrue(resource.getApplyPrefix())

    def test_cssregistry__shop__title(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertIsNone(resource.getTitle())

    def test_cssregistry__shop__authenticated(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertFalse(resource.getAuthenticated())

    def test_cssregistry__shop__compression(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertEqual(resource.getCompression(), 'safe')

    def test_cssregistry__shop__conditionalcomment(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertEqual(resource.getConditionalcomment(), '')

    def test_cssregistry__shop__cookable(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertTrue(resource.getCookable())

    def test_cssregistry__shop__enabled(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertTrue(resource.getEnabled())

    def test_cssregistry__shop__expression(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertEqual(resource.getExpression(), '')

    def test_cssregistry__shop__media(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertIsNone(resource.getMedia())

    def test_cssregistry__shop__rel(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertEqual(resource.getRel(), 'stylesheet')

    def test_cssregistry__shop__rendering(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertEqual(resource.getRendering(), 'link')

    def test_cssregistry__shop__applyPrefix(self):
        resource = self.get_css_resource('++resource++slt.theme/css/shop.css')
        self.assertTrue(resource.getApplyPrefix())

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-slt.theme:default'), u'10')

    def test_metadata__installed__sll_basetheme(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.basetheme'))

    def test_metadata__installed__sll_carousel(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.carousel'))

    def test_metadata__installed__slt_content(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('slt.content'))

    def test_metadata__installed__slt_portlet(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('slt.portlet'))

    def get_record(self, name):
        """Get registry record based on """
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        return getUtility(IRegistry).records.get(name)

    def test_registry_record__slt_theme_articles_feed_on_top_page__field__type(self):
        from plone.registry.field import Int
        record = self.get_record('slt.theme.articles_feed_on_top_page')
        self.assertIsInstance(record.field, Int)

    def test_registry_record__slt_theme_articles_feed_on_top_page__field__title(self):
        record = self.get_record('slt.theme.articles_feed_on_top_page')
        self.assertEqual(record.field.title, u'Articles feed on top page')

    def test_registry_record__slt_theme_articles_feed_on_top_page__field__min(self):
        record = self.get_record('slt.theme.articles_feed_on_top_page')
        self.assertEqual(record.field.min, 0)

    def test_registry_record__slt_theme_articles_feed_on_top_page(self):
        record = self.get_record('slt.theme.articles_feed_on_top_page')
        self.assertEqual(record.value, 0)

    def test_rolemap__slt_theme_Show_byline__rolesOfPermission(self):
        permission = "slt.theme: Show byline"
        self.assertEqual(get_roles(self.portal, permission), [
            'Manager',
            'Site Administrator'])

    def test_rolemap__slt_theme_Show_byline__acquiredRolesAreUsedBy(self):
        permission = "slt.theme: Show byline"
        self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), '')

    def get_ctype(self, name):
        """Returns content type info.

        :param name: Name of content type.
        :type name: test_types__Plone_Site__filter_content_types
        """
        types = getToolByName(self.portal, 'portal_types')
        return types.getTypeInfo(name)

    def test_types__Plone_Site__immediate_view(self):
        ctype = self.get_ctype('Plone Site')
        self.assertEqual(ctype.immediate_view, 'slt-view')

    def test_types__Plone_Site__default_view(self):
        ctype = self.get_ctype('Plone Site')
        self.assertEqual(ctype.default_view, 'slt-view')

    def test_types__Plone_Site__view_methods(self):
        ctype = self.get_ctype('Plone Site')
        self.assertEqual(ctype.view_methods, ('slt-view',))

    def test_viewlets__order__collective_base_viewlet_manager_base_form(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "collective.base.viewlet-manager.base-form"
        skinname = "*"
        self.assertEqual(storage.getOrder(manager, skinname), (
            u'collective.cart.core.viewlet.add-to-cart',
            u'collective.cart.shopping.viewlet.body-text',
            u'collective.cart.shopping.viewlet.articles-in-article',
            u'collective.cart.shopping.viewlet.add-subtract-stock',
            u'collective.cart.shopping.viewlet.stock-listing',
            u'collective.cart.core.viewlet.cart-article-listing',
            u'collective.cart.shopping.viewlet.cart-articles-total',
            u'collective.cart.shopping.viewlet.cart-check-out-buttons',
            u'collective.cart.shopping.viewlet.billing-and-shipping-billing-address',
            u'collective.cart.shopping.viewlet.billing-and-shipping-shipping-address',
            u'collective.cart.shopping.viewlet.billing-and-shipping-shipping-methods',
            u'slt.theme.viewlet.billing-and-shipping-registration-number',
            u'collective.cart.shopping.viewlet.billing-and-shipping-check-out-buttons',
            u'collective.cart.shopping.viewlet.order-confirmation-cart-article-listing',
            u'collective.cart.shopping.viewlet.order-confirmation-shipping-method',
            u'collective.cart.shopping.viewlet.order-confirmation-total',
            u'slt.theme.viewlet.order-confirmation-registration-number',
            u'collective.cart.shopping.viewlet.order-confirmation-terms',
            u'collective.cart.shopping.viewlet.order-confirmation-check-out-buttons',
            u'slt.theme.viewlet.add-address',
            u'slt.theme.viewlet.address-listing',
            u'slt.theme.viewlet.order-listing'))

    def test_viewlets__hidden__plone_portalfooter(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portalfooter"
        skinname = "*"
        for viewlet in (
            u'plone.colophon',
            u'plone.footer',
            u'plone.site_actions',
            u'sll.basetheme.footer.message',
            u'sll.basetheme.footer.subfolders'):
            self.assertIn(viewlet, storage.getHidden(manager, skinname))

    def test_viewlets__order__plone_portalfooter(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portalfooter"
        skinname = "*"
        self.assertEqual(storage.getOrder(manager, skinname), (
            u'plone.footer',
            u'plone.colophon',
            u'plone.site_actions',
            u'sll.basetheme.footer.subfolders',
            u'sll.basetheme.footer.info'))

    def uninstall_package(self):
        """Uninstall package: slt.theme."""
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['slt.theme'])

    def test_uninstall__package(self):
        self.uninstall_package()
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertFalse(installer.isProductInstalled('slt.theme'))

    def test_uninstall__actions__object_buttons__feed_to_shop_top(self):
        self.uninstall_package()
        self.assertIsNone(self.get_action('feed_to_shop_top'))

    def test_uninstall__actions__object_buttons__unfeed_from_shop_top(self):
        self.uninstall_package()
        self.assertIsNone(self.get_action('unfeed_from_shop_top'))

    def test_uninstall__browserlayer(self):
        self.uninstall_package()
        from slt.theme.browser.interfaces import ISltThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(ISltThemeLayer, utils.registered_layers())

    def test_uninstall__cssregistry_main(self):
        self.uninstall_package()
        resources = set(getToolByName(self.portal, 'portal_css').getResourceIds())
        self.assertNotIn('++resource++slt.theme/css/main.css', resources)

    def test_uninstall__cssregistry_shop(self):
        self.uninstall_package()
        resources = set(getToolByName(self.portal, 'portal_css').getResourceIds())
        self.assertNotIn('++resource++slt.theme/css/shop.css', resources)

    def test_unintall__types__Plone_Site__immediate_view(self):
        self.uninstall_package()
        ctype = self.get_ctype('Plone Site')
        self.assertEqual(ctype.immediate_view, 'slt-view')

    def test_unintall__types__Plone_Site__default_view(self):
        self.uninstall_package()
        ctype = self.get_ctype('Plone Site')
        self.assertEqual(ctype.default_view, 'slt-view')

    def test_unintall__types__Plone_Site__view_methods(self):
        self.uninstall_package()
        ctype = self.get_ctype('Plone Site')
        self.assertEqual(ctype.view_methods, ('slt-view',))
