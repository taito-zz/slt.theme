from slt.theme.browser.interfaces import IShopView
from slt.theme.browser.template import ShopView
from slt.theme.tests.base import IntegrationTestCase


class ShopViewTestCase(IntegrationTestCase):
    """TestCase for ShopView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseView
        self.assertTrue(issubclass(ShopView, BaseView))
        from collective.base.interfaces import IBaseFormView
        self.assertTrue(issubclass(IShopView, IBaseFormView))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(ShopView)
        self.assertTrue(verifyObject(IShopView, instance))
