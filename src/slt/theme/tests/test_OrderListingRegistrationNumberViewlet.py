from slt.theme.browser.interfaces import IOrderListingRegistrationNumberViewlet
from slt.theme.browser.viewlet import OrderListingRegistrationNumberViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class OrderListingRegistrationNumberViewletTestCase(IntegrationTestCase):
    """TestCase for OrderListingRegistrationNumberViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(issubclass(OrderListingRegistrationNumberViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IOrderListingRegistrationNumberViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(OrderListingRegistrationNumberViewlet)
        self.assertTrue(verifyObject(IOrderListingRegistrationNumberViewlet, instance))

    def test___handle_repeated(self):
        instance = self.create_viewlet(OrderListingRegistrationNumberViewlet)
        obj = mock.Mock()
        obj.registration_number = 'RN'
        item = {'obj': obj}
        instance._handle_repeated(item)
        self.assertEqual(instance.registration_number, 'RN')
