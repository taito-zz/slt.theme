from Products.CMFCore.utils import getToolByName
from slt.theme.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_update_viewlets(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.abovecontenttitle"
        skinname = "Plone Default"
        storage.setHidden(manager, skinname, ())

        self.assertEqual(len(storage.getHidden(manager, skinname)), 0)

        from slt.theme.upgrades import update_viewlets
        update_viewlets(self.portal)

        self.assertEqual(storage.getHidden(manager, skinname), (u'collective.cart.core.add.to.cart',))
