from collective.cart.core.interfaces import IShoppingSiteRoot
from slt.theme.browser.template import OrdersView
from slt.theme.tests.base import IntegrationTestCase
from zope.interface import alsoProvides


class OrdersViewTestCase(IntegrationTestCase):
    """TestCase for OrdersView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseMemberAreaView
        self.assertTrue(issubclass(OrdersView, BaseMemberAreaView))

    def test_name(self):
        self.assertEqual(getattr(OrdersView, 'grokcore.component.directive.name'), 'view')

    def test_template(self):
        self.assertEqual(getattr(OrdersView, 'grokcore.view.directive.template'), 'orders')

    def test_carts(self):
        instance = self.create_view(OrdersView)
        self.assertEqual(len(instance.carts), 0)

        alsoProvides(self.portal, IShoppingSiteRoot)
        self.assertEqual(len(instance.carts), 0)

        self.create_content('collective.cart.core.Cart', id='1')
        self.assertEqual(len(instance.carts), 1)

        self.create_content('collective.cart.core.Cart', id='2')
        self.assertEqual(len(instance.carts), 2)

        instance.request.form = {'order_number': '2'}
        self.assertEqual(len(instance.carts), 1)
        self.assertEqual(instance.carts[0]['id'], '2')

    def test_class_collapsible(self):
        instance = self.create_view(OrdersView)
        self.assertEqual(instance.class_collapsible, 'collapsible collapsedOnLoad')

        self.create_content('collective.cart.core.Cart', id='1')
        self.assertEqual(instance.class_collapsible, 'collapsible')
