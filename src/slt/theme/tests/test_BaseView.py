from slt.theme.browser.template import BaseView

import unittest


class BaseViewTestCase(unittest.TestCase):
    """TestCase for BaseView"""

    def test_templatedir(self):
        from slt.theme.browser import template
        self.assertEqual(getattr(template, 'grokcore.view.directive.templatedir'), 'templates')

    def test_subclass(self):
        from five.grok import View
        self.assertTrue(issubclass(BaseView, View))

    def test_baseclass(self):
        self.assertTrue(getattr(BaseView, 'martian.martiandirective.baseclass'))

    def test_layer(self):
        from slt.theme.browser.interfaces import ISltThemeLayer
        self.assertEqual(getattr(BaseView, 'grokcore.view.directive.layer'), ISltThemeLayer)

    def test_require(self):
        self.assertEqual(getattr(BaseView, 'grokcore.security.directive.require'), ['zope2.View'])
