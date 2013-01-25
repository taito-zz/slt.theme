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
    def test_reimport_rolemap(self, reimport_profile):
        from slt.theme.upgrades import reimport_rolemap
        reimport_rolemap(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-slt.theme:default', 'rolemap')
