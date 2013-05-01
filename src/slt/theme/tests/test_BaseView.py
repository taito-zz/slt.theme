from slt.theme.tests.base import IntegrationTestCase
from slt.theme.browser.template import BaseView

import mock


class BaseViewTestCase(IntegrationTestCase):
    """TestCase for BaseView"""

    def test_subclass(self):
        from collective.base.view import BaseFormView
        self.assertTrue(issubclass(BaseView, BaseFormView))

    def test___call__(self):
        instance = self.create_view(BaseView)
        instance.template = mock.Mock()
        self.assertEqual(instance(), instance.template())

    def test_title(self):
        instance = self.create_view(BaseView)
        instance.context.Title = mock.Mock(return_value='TITLE')
        self.assertEqual(instance.title(), 'TITLE')

    def test_description(self):
        instance = self.create_view(BaseView)
        instance.context.Description = mock.Mock(return_value='DESCRIPTION')
        self.assertEqual(instance.description(), 'DESCRIPTION')
