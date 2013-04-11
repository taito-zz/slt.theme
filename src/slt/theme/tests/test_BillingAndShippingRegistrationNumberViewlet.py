from slt.theme.browser.viewlet import BillingAndShippingRegistrationNumberViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class BillingAndShippingRegistrationNumberViewletTestCase(IntegrationTestCase):
    """TestCase for BillingAndShippingRegistrationNumberViewlet"""

    def test_subclass(self):
        from collective.cart.shopping.browser.viewlet import BaseShoppingSiteRootViewlet
        self.assertTrue(BillingAndShippingRegistrationNumberViewlet, BaseShoppingSiteRootViewlet)

    def test_name(self):
        self.assertEqual(getattr(BillingAndShippingRegistrationNumberViewlet, 'grokcore.component.directive.name'), 'slt.theme.billing-and-shipping-registration-number')

    def test_template(self):
        self.assertEqual(getattr(BillingAndShippingRegistrationNumberViewlet, 'grokcore.view.directive.template'), 'billing-and-shipping-registration-number')

    def test_viewletmanager(self):
        from collective.cart.shopping.browser.viewlet import BillingAndShippingViewletManager
        self.assertEqual(getattr(BillingAndShippingRegistrationNumberViewlet, 'grokcore.viewlet.directive.viewletmanager'), BillingAndShippingViewletManager)

    @mock.patch('slt.theme.browser.viewlet.IShoppingSite')
    def test_registration_number(self, IShoppingSite):
        instance = self.create_viewlet(BillingAndShippingRegistrationNumberViewlet)
        IShoppingSite().cart = {}
        instance.context.restrictedTraverse = mock.Mock()
        instance.context.restrictedTraverse().member().getProperty.return_value = None
        self.assertIsNone(instance.registration_number)

        instance.context.restrictedTraverse().member().getProperty.return_value = 'RN1'
        self.assertEqual(instance.registration_number, 'RN1')

        IShoppingSite().cart = {'registration_number': 'RN2'}
        self.assertEqual(instance.registration_number, 'RN2')

    @mock.patch('slt.theme.browser.viewlet.IShoppingSite')
    def test_update(self, IShoppingSite):
        instance = self.create_viewlet(BillingAndShippingRegistrationNumberViewlet)
        instance.update()
        self.assertEqual(IShoppingSite().update_cart.call_count, 0)

        instance.request.form = {'form.to.confirmation': True}
        instance.update()
        self.assertEqual(IShoppingSite().update_cart.call_count, 0)

        instance.request.form = {'form.to.confirmation': True, 'registration_number': ' RN '}
        instance.update()
        self.assertEqual(IShoppingSite().update_cart.call_count, 1)
        IShoppingSite().update_cart.assert_called_with('registration_number', 'RN')
