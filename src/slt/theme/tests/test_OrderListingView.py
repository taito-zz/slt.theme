from slt.theme.browser.interfaces import IOrderListingView
from slt.theme.browser.template import OrderListingView
from slt.theme.tests.base import IntegrationTestCase


class OrderListingViewTestCase(IntegrationTestCase):
    """TestCase for OrderListingView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseView
        self.assertTrue(issubclass(OrderListingView, BaseView))
        from collective.base.interfaces import IBaseFormView
        self.assertTrue(issubclass(IOrderListingView, IBaseFormView))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(OrderListingView)
        self.assertTrue(verifyObject(IOrderListingView, instance))
