from slt.theme.tests.base import IntegrationTestCase

import mock


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_reimport_registry(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        registry['slt.theme.articles_feed_on_top_page'] = 4
        self.assertEqual(registry['slt.theme.articles_feed_on_top_page'], 4)

        from slt.theme.upgrades import reimport_registry
        reimport_registry(self.portal)

        self.assertEqual(registry['slt.theme.articles_feed_on_top_page'], 0)

    def test_reimport_viewlets(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.abovecontenttitle"
        skinname = "Plone Default"
        storage.setHidden(manager, skinname, ())

        self.assertEqual(len(storage.getHidden(manager, skinname)), 0)

        from slt.theme.upgrades import reimport_viewlets
        reimport_viewlets(self.portal)

        self.assertEqual(storage.getHidden(manager, skinname), (u'collective.cart.core.add.to.cart',))

    @mock.patch('slt.theme.upgrades.reimport_profile')
    def test_reimport_cssregistry(self, reimport_profile):
        from slt.theme.upgrades import reimport_cssregistry
        reimport_cssregistry(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-slt.theme:default', 'cssregistry')

    @mock.patch('slt.theme.upgrades.reimport_profile')
    def test_reimport_memberdata_properties(self, reimport_profile):
        from slt.theme.upgrades import reimport_memberdata_properties
        reimport_memberdata_properties(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-slt.theme:default', 'memberdata-properties')

    @mock.patch('slt.theme.upgrades.reimport_profile')
    def test_reimport_rolemap(self, reimport_profile):
        from slt.theme.upgrades import reimport_rolemap
        reimport_rolemap(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-slt.theme:default', 'rolemap')

    def test_clean_viewlets(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = 'collective.cart.shopping.billing.shipping.manager'
        skinname = 'Plone Default'
        storage.setHidden(manager, skinname, [u'viewlet1'])
        storage.setOrder(manager, skinname, [u'viewlet2'])

        self.assertEqual(storage.getHidden(manager, skinname), (u'viewlet1',))
        self.assertEqual(storage.getOrder(manager, skinname), (u'viewlet2',))

        from slt.theme.upgrades import clean_viewlets
        clean_viewlets(manager, skinname)

        self.assertEqual(storage.getHidden(manager, skinname), ())
        self.assertEqual(storage.getOrder(manager, skinname), (u'collective.cart.shopping.billing.info',))

        skinname = u'*'
        storage.setHidden(manager, skinname, [u'viewlet3'])
        storage.setOrder(manager, skinname, [u'viewlet4'])

        self.assertEqual(storage.getHidden(manager, skinname), (u'viewlet3',))
        self.assertEqual(storage.getOrder(manager, skinname), (u'viewlet4',))

    @mock.patch('slt.theme.upgrades.clean_viewlets')
    def test_clean_viewlets_from_collective_cart_shopping_billing_shipping_manager(self, clean_viewlets):
        from slt.theme.upgrades import clean_viewlets_from_collective_cart_shopping_billing_shipping_manager
        clean_viewlets_from_collective_cart_shopping_billing_shipping_manager(self.portal)
        self.assertEqual(clean_viewlets.call_args_list, [
            [(u'collective.cart.shopping.billing.shipping.manager', u'Plone Default')],
            [(u'collective.cart.shopping.billing.shipping.manager', u'Sunburst Theme')],
            [(u'collective.cart.shopping.billing.shipping.manager', u'*')]])
