from slt.theme.browser.template import ShopView

import unittest


class ShopViewTestCase(unittest.TestCase):
    """TestCase for ShopView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseView
        self.assertTrue(issubclass(ShopView, BaseView))

    def test_context(self):
        from Products.CMFPlone.interfaces import IPloneSiteRoot
        self.assertEqual(getattr(ShopView, 'grokcore.component.directive.context'), IPloneSiteRoot)

    def test_name(self):
        self.assertEqual(getattr(ShopView, 'grokcore.component.directive.name'), 'slt-view')

    def test_template(self):
        self.assertEqual(getattr(ShopView, 'grokcore.view.directive.template'), 'shop')
