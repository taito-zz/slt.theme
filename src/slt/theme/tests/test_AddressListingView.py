from slt.theme.browser.interfaces import IAddressListingView
from slt.theme.browser.view import AddressListingView
from slt.theme.tests.base import IntegrationTestCase


class AddressListingViewTestCase(IntegrationTestCase):
    """TestCase for AddressListingView"""

    def test_subclass(self):
        from slt.theme.browser.view import BaseView
        self.assertTrue(issubclass(AddressListingView, BaseView))
        from collective.base.interfaces import IBaseFormView
        self.assertTrue(issubclass(IAddressListingView, IBaseFormView))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(AddressListingView)
        self.assertTrue(verifyObject(IAddressListingView, instance))
