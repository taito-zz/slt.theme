from slt.theme.browser.template import ToCustomerOrderMailTemplateView

import unittest


class ToCustomerOrderMailTemplateViewTestCase(unittest.TestCase):
    """TestCase for ToCustomerOrderMailTemplateView"""

    def test_subclass(self):
        from collective.cart.shopping.browser.template import ToCustomerOrderMailTemplateView as Base
        self.assertTrue(issubclass(ToCustomerOrderMailTemplateView, Base))

    def test_template(self):
        self.assertEqual(ToCustomerOrderMailTemplateView.template.filename.split('/')[-1], 'order-mail-template.pt')
