from slt.theme.browser.viewlet import BaseViewletManager

import unittest


class BaseViewletManagerTestCase(unittest.TestCase):
    """TestCase for BaseViewletManager"""

    def test_subclass(self):
        from five.grok import ViewletManager
        from plone.app.viewletmanager.manager import OrderedViewletManager
        self.assertTrue(issubclass(BaseViewletManager, (OrderedViewletManager, ViewletManager)))

    def test_baseclass(self):
        self.assertTrue(getattr(BaseViewletManager, 'martian.martiandirective.baseclass'))

    def test_layer(self):
        from slt.theme.browser.interfaces import ISltThemeLayer
        self.assertEqual(getattr(BaseViewletManager, 'grokcore.view.directive.layer'), ISltThemeLayer)
