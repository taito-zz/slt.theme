from slt.theme.browser.interfaces import IOrderConfirmationRegistrationNumberViewlet
from slt.theme.browser.viewlet import OrderConfirmationRegistrationNumberViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class OrderConfirmationRegistrationNumberViewletTestCase(IntegrationTestCase):
    """TestCase for OrderConfirmationRegistrationNumberViewlet"""

    def test_subclass(self):
        from plone.app.layout.viewlets.common import ViewletBase as Base
        self.assertTrue(issubclass(OrderConfirmationRegistrationNumberViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IOrderConfirmationRegistrationNumberViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(OrderConfirmationRegistrationNumberViewlet)
        self.assertTrue(verifyObject(IOrderConfirmationRegistrationNumberViewlet, instance))

    @mock.patch('slt.theme.browser.viewlet.IShoppingSite')
    def test_registration_number(self, IShoppingSite):
        instance = self.create_viewlet(OrderConfirmationRegistrationNumberViewlet)
        IShoppingSite().cart.return_value = None
        self.assertIsNone(instance.registration_number())

        IShoppingSite().cart.return_value = {'registration_number': 'RN'}
        self.assertEqual(instance.registration_number(), 'RN')
