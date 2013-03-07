from slt.theme.browser.viewlet import BaseViewlet

import unittest


class BaseViewletTestCase(unittest.TestCase):
    """TestCase for BaseViewlet"""

    def test_templatedir(self):
        from slt.theme.browser import viewlet
        self.assertEqual(getattr(viewlet, 'grokcore.view.directive.templatedir'), 'viewlets')

    def test_subclass(self):
        from five.grok import Viewlet
        self.assertTrue(issubclass(BaseViewlet, Viewlet))

    def test_baseclass(self):
        self.assertTrue(getattr(BaseViewlet, 'martian.martiandirective.baseclass'))

    def test_layer(self):
        from slt.theme.browser.interfaces import ISltThemeLayer
        self.assertEqual(getattr(BaseViewlet, 'grokcore.view.directive.layer'), ISltThemeLayer)

    def test_require(self):
        self.assertEqual(getattr(BaseViewlet, 'grokcore.security.directive.require'), ['zope2.View'])
