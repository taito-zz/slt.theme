from slt.theme.browser.interfaces import IBillingAndShippingRegistrationNumberViewlet
from slt.theme.browser.viewlet import BillingAndShippingRegistrationNumberViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class BillingAndShippingRegistrationNumberViewletTestCase(IntegrationTestCase):
    """TestCase for BillingAndShippingRegistrationNumberViewlet"""

    def test_subclass(self):
        from plone.app.layout.viewlets.common import ViewletBase as Base
        self.assertTrue(issubclass(BillingAndShippingRegistrationNumberViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IBillingAndShippingRegistrationNumberViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(BillingAndShippingRegistrationNumberViewlet)
        self.assertTrue(verifyObject(IBillingAndShippingRegistrationNumberViewlet, instance))

    @mock.patch('slt.theme.browser.viewlet.IShoppingSite')
    def test_registration_number(self, IShoppingSite):
        instance = self.create_viewlet(BillingAndShippingRegistrationNumberViewlet)
        IShoppingSite().cart.return_value = {}
        instance.context.restrictedTraverse = mock.Mock()
        instance.context.restrictedTraverse().member().getProperty.return_value = None
        self.assertIsNone(instance.registration_number())

        instance.context.restrictedTraverse().member().getProperty.return_value = 'RN1'
        self.assertEqual(instance.registration_number(), 'RN1')

        IShoppingSite().cart.return_value = {'registration_number': 'RN2'}
        self.assertEqual(instance.registration_number(), 'RN2')

    @mock.patch('slt.theme.browser.viewlet.IShoppingSite')
    def test_update(self, IShoppingSite):
        instance = self.create_viewlet(BillingAndShippingRegistrationNumberViewlet)
        instance.update()
        self.assertEqual(IShoppingSite().update_cart.call_count, 0)

        instance.request.form = {'form.buttons.CheckOut': True}
        instance.update()
        self.assertEqual(IShoppingSite().update_cart.call_count, 0)

        instance.request.form = {'form.buttons.CheckOut': True, 'registration_number': ' RN '}
        instance.update()
        self.assertEqual(IShoppingSite().update_cart.call_count, 1)
        IShoppingSite().update_cart.assert_called_with('registration_number', 'RN')
