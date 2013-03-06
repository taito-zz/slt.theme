from slt.theme.browser.template import BaseMemberAreaView

import unittest


class BaseMemberAreaViewTestCase(unittest.TestCase):
    """TestCase for BaseMemberAreaView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseView
        self.assertTrue(issubclass(BaseMemberAreaView, BaseView))

    def test_baseclass(self):
        self.assertTrue(getattr(BaseMemberAreaView, 'martian.martiandirective.baseclass'))

    def test_context(self):
        from slt.content.schema import IMemberArea
        self.assertEqual(getattr(BaseMemberAreaView, 'grokcore.component.directive.context'), IMemberArea)
