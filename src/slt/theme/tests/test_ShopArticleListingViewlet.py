# -*- coding: utf-8 -*-
from slt.theme.browser.interfaces import IShopArticleListingViewlet
from slt.theme.browser.viewlet import ShopArticleListingViewlet
from slt.theme.tests.base import IntegrationTestCase


class ShopArticleListingViewletTestCase(IntegrationTestCase):
    """TestCase for ShopArticleListingViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(ShopArticleListingViewlet, Base)
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IShopArticleListingViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(ShopArticleListingViewlet)
        self.assertTrue(verifyObject(IShopArticleListingViewlet, instance))
