from slt.theme.browser.viewlet import OrderConfirmationRegistrationNumberViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class OrderConfirmationRegistrationNumberViewletTestCase(IntegrationTestCase):
    """TestCase for OrderConfirmationRegistrationNumberViewlet"""

    def test_subclass(self):
        from collective.cart.shopping.browser.viewlet import BaseOrderConfirmationViewlet
        self.assertTrue(OrderConfirmationRegistrationNumberViewlet, BaseOrderConfirmationViewlet)

    def test_layer(self):
        from slt.theme.browser.interfaces import ISltThemeLayer
        self.assertEqual(getattr(OrderConfirmationRegistrationNumberViewlet, 'grokcore.view.directive.layer'), ISltThemeLayer)

    def test_name(self):
        self.assertEqual(getattr(OrderConfirmationRegistrationNumberViewlet, 'grokcore.component.directive.name'), 'slt.theme.confirmation-registration-number')

    def test_template(self):
        self.assertEqual(getattr(OrderConfirmationRegistrationNumberViewlet, 'grokcore.view.directive.template'), 'registration-number')

    @mock.patch('slt.theme.browser.viewlet.IShoppingSite')
    def test_registration_number(self, IShoppingSite):
        instance = self.create_viewlet(OrderConfirmationRegistrationNumberViewlet)
        IShoppingSite().cart = None
        self.assertIsNone(instance.registration_number)

        IShoppingSite().cart = {'registration_number': 'RN'}
        self.assertEqual(instance.registration_number, 'RN')
