from slt.theme.browser.interfaces import IBillingAndShippingBillingAddressViewlet
from slt.theme.browser.viewlet import BillingAndShippingBillingAddressViewlet
from slt.theme.tests.base import IntegrationTestCase


class BillingAndShippingBillingAddressViewletTestCase(IntegrationTestCase):
    """TestCase for BillingAndShippingBillingAddressViewlet"""

    def test_subclass(self):
        from collective.cart.shopping.browser.viewlet import BillingAndShippingBillingAddressViewlet as Base
        self.assertTrue(issubclass(BillingAndShippingBillingAddressViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IBillingAndShippingBillingAddressViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(BillingAndShippingBillingAddressViewlet)
        self.assertTrue(verifyObject(IBillingAndShippingBillingAddressViewlet, instance))
