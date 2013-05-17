from collective.cart.shopping.browser.interfaces import IOrderListingViewletManager
from slt.theme.browser.viewletmanager import OrderListingViewletManager
from slt.theme.tests.base import IntegrationTestCase


class OrderListingViewletManagerTestCase(IntegrationTestCase):
    """TestCase for OrderListingViewletManager"""

    def test_subclass(self):
        from collective.cart.shopping.browser.viewletmanager import OrderListingViewletManager as Base
        self.assertTrue(issubclass(OrderListingViewletManager, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewletmanager(OrderListingViewletManager)
        self.assertTrue(verifyObject(IOrderListingViewletManager, instance))

    def test__orders(self):
        instance = self.create_viewletmanager(OrderListingViewletManager)
        self.assertEqual(len(instance._orders()), 0)

        container = self.create_content('collective.cart.core.OrderContainer')
        self.create_content('collective.cart.core.Order', container, id='1')
        self.create_content('collective.cart.core.Order', container, id='2')
        instance = self.create_viewletmanager(OrderListingViewletManager, container)
        self.assertEqual(len(instance._orders()), 2)

        instance.request.form = {'order_number': '2'}
        self.assertEqual(len(instance._orders()), 1)
