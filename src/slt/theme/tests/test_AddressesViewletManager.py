from slt.theme.browser.viewlet import AddressesViewletManager

import unittest


class AddressesViewletManagerTestCase(unittest.TestCase):
    """TestCase for AddressesViewletManager"""

    def test_subclass(self):
        from slt.theme.browser.viewlet import BaseViewletManager
        self.assertTrue(issubclass(AddressesViewletManager, BaseViewletManager))

    def test_context(self):
        from zope.interface import Interface
        self.assertEqual(getattr(AddressesViewletManager, 'grokcore.component.directive.context'), Interface)

    def test_name(self):
        self.assertEqual(getattr(AddressesViewletManager, 'grokcore.component.directive.name'), 'slt.theme.addresses.viewletmanager')
