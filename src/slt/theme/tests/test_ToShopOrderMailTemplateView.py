from slt.theme.browser.view import ToShopOrderMailTemplateView

import unittest


class ToShopOrderMailTemplateViewTestCase(unittest.TestCase):
    """TestCase for ToShopOrderMailTemplateView"""

    def test_subclass(self):
        from collective.cart.shopping.browser.view import ToShopOrderMailTemplateView as Base
        self.assertTrue(issubclass(ToShopOrderMailTemplateView, Base))

    def test_template(self):
        self.assertEqual(ToShopOrderMailTemplateView.template.filename.split('/')[-1], 'order-mail-template.pt')
