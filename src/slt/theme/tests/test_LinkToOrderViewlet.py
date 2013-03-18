from slt.theme.browser.viewlet import LinkToOrderViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class LinkToOrderViewletTestCase(IntegrationTestCase):
    """TestCase for LinkToOrderViewlet"""

    def test_subclass(self):
        from slt.theme.browser.viewlet import BaseViewlet
        self.assertTrue(LinkToOrderViewlet, BaseViewlet)

    def test_context(self):
        from collective.cart.core.interfaces import IShoppingSiteRoot
        self.assertEqual(getattr(LinkToOrderViewlet, 'grokcore.component.directive.context'), IShoppingSiteRoot)

    def test_name(self):
        self.assertEqual(getattr(LinkToOrderViewlet, 'grokcore.component.directive.name'), 'slt.theme.link.to.order')

    def test_template(self):
        self.assertEqual(getattr(LinkToOrderViewlet, 'grokcore.view.directive.template'), 'link-to-order')

    def test_viewletmanager(self):
        from slt.theme.browser.viewlet import ThanksBelowContentViewletManager
        self.assertEqual(getattr(LinkToOrderViewlet, 'grokcore.viewlet.directive.viewletmanager'), ThanksBelowContentViewletManager)

    @mock.patch('slt.theme.browser.viewlet.getToolByName')
    def test_order_url(self, getToolByName):
        view = mock.Mock()
        view.cart_id = '2'
        instance = self.create_viewlet(LinkToOrderViewlet, view=view)
        getToolByName().getHomeUrl.return_value = 'home_url'
        self.assertEqual(instance.order_url, 'home_url?order_number=2')
