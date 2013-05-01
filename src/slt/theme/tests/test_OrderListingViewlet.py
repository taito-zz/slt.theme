# -*- coding: utf-8 -*-
from collective.cart.core.interfaces import IShoppingSiteRoot
from slt.theme.browser.interfaces import IOrderListingViewlet
from slt.theme.browser.viewlet import OrderListingViewlet
from slt.theme.tests.base import IntegrationTestCase
from zope.interface import alsoProvides


class OrderListingViewletTestCase(IntegrationTestCase):
    """TestCase for OrderListingViewlet"""

    def test_subclass(self):
        from plone.app.layout.viewlets.common import ViewletBase as Base
        self.assertTrue(issubclass(OrderListingViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IOrderListingViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(OrderListingViewlet)
        self.assertTrue(verifyObject(IOrderListingViewlet, instance))

    def test_orders(self):
        instance = self.create_viewlet(OrderListingViewlet)
        self.assertEqual(len(instance.orders()), 0)

        alsoProvides(self.portal, IShoppingSiteRoot)
        self.assertEqual(len(instance.orders()), 0)

        self.create_content('collective.cart.core.Order', id='1')
        self.assertEqual(len(instance.orders()), 1)

        self.create_content('collective.cart.core.Order', id='2')
        self.assertEqual(len(instance.orders()), 2)

        instance.request.form = {'order_number': '2'}
        self.assertEqual(len(instance.orders()), 1)
        self.assertEqual(instance.orders()[0]['id'], '2')

    def test_class_collapsible(self):
        instance = self.create_viewlet(OrderListingViewlet)
        self.assertEqual(instance.class_collapsible(), 'collapsible collapsedOnLoad')

        self.create_content('collective.cart.core.Order', id='1')
        self.assertEqual(instance.class_collapsible(), 'collapsible')
