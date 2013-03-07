from slt.theme.browser.viewlet import ShopTopViewletManager

import unittest


class ShopTopViewletManagerTestCase(unittest.TestCase):
    """TestCase for ShopTopViewletManager"""

    def test_subclass(self):
        from slt.theme.browser.viewlet import BaseViewletManager
        self.assertTrue(issubclass(ShopTopViewletManager, BaseViewletManager))

    def test_context(self):
        from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
        self.assertEqual(getattr(ShopTopViewletManager, 'grokcore.component.directive.context'), IPloneSiteRoot)

    def test_name(self):
        self.assertEqual(getattr(ShopTopViewletManager, 'grokcore.component.directive.name'), 'slt.theme.shop.top.viewletmanager')
