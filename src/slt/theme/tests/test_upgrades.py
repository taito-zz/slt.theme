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
        reimport_registry(self.portal.portal_setup)

        self.assertEqual(registry['slt.theme.articles_feed_on_top_page'], 0)

    def test_reimport_viewlets(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portalfooter"
        skinname = "*"
        storage.setHidden(manager, skinname, (u'plone.colophon',))
        self.assertEqual(len(storage.getHidden(manager, skinname)), 1)

        from slt.theme.upgrades import reimport_viewlets
        reimport_viewlets(self.portal.portal_setup)
        self.assertEqual(len(storage.getHidden(manager, skinname)), 5)

    def test_reimport_actions(self):
        setup = mock.Mock()
        from slt.theme.upgrades import reimport_actions
        reimport_actions(setup)
        setup.runImportStepFromProfile.assert_called_with(
            'profile-slt.theme:default', 'actions', run_dependencies=False, purge_old=False)

    def test_reimport_cssregistry(self):
        setup = mock.Mock()
        from slt.theme.upgrades import reimport_cssregistry
        reimport_cssregistry(setup)
        setup.runImportStepFromProfile.assert_called_with(
            'profile-slt.theme:default', 'cssregistry', run_dependencies=False, purge_old=False)

    def test_reimport_jsregistry(self):
        setup = mock.Mock()
        from slt.theme.upgrades import reimport_jsregistry
        reimport_jsregistry(setup)
        setup.runImportStepFromProfile.assert_called_with(
            'profile-slt.theme:default', 'jsregistry', run_dependencies=False, purge_old=False)

    def test_reimport_memberdata_properties(self):
        setup = mock.Mock()
        from slt.theme.upgrades import reimport_memberdata_properties
        reimport_memberdata_properties(setup)
        setup.runImportStepFromProfile.assert_called_with(
            'profile-slt.theme:default', 'memberdata-properties', run_dependencies=False, purge_old=False)

    def test_reimport_rolemap(self):
        setup = mock.Mock()
        from slt.theme.upgrades import reimport_rolemap
        reimport_rolemap(setup)
        setup.runImportStepFromProfile.assert_called_with(
            'profile-slt.theme:default', 'rolemap', run_dependencies=False, purge_old=False)

    def test_clean_viewlets(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = 'collective.base.viewlet-manager.base-form'
        skinname = 'Plone Default'
        storage.setHidden(manager, skinname, [u'viewlet1'])
        storage.setOrder(manager, skinname, [u'viewlet2'])

        self.assertEqual(storage.getHidden(manager, skinname), (u'viewlet1',))
        self.assertEqual(storage.getOrder(manager, skinname), (u'viewlet2',))

        from slt.theme.upgrades import clean_viewlets
        clean_viewlets(manager, skinname)

        self.assertEqual(storage.getHidden(manager, skinname), ())
        self.assertEqual(storage.getOrder(manager, skinname), ())

        skinname = u'*'
        storage.setHidden(manager, skinname, [u'viewlet3'])
        storage.setOrder(manager, skinname, [u'viewlet4'])

        self.assertEqual(storage.getHidden(manager, skinname), (u'viewlet3',))
        self.assertEqual(storage.getOrder(manager, skinname), (u'viewlet4',))
