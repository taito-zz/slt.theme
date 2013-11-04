from slt.theme.browser.view import PwresetFinishView
from slt.theme.tests.base import IntegrationTestCase

import mock


class PwresetFinishViewTestCase(IntegrationTestCase):
    """TestCase for PwresetFinishView"""

    def test_subclass(self):
        from Products.Five import BrowserView
        self.assertTrue(issubclass(PwresetFinishView, BrowserView))

    @mock.patch('slt.theme.browser.view.IStatusMessage')
    def test___call__(self, IStatusMessage):
        instance = self.create_view(PwresetFinishView)
        instance.context.absolute_url = mock.Mock(return_value='portal_url')
        self.assertEqual(instance(), 'portal_url/login_form?came_from=portal_url')
        IStatusMessage().addStatusMessage.assert_called_with(u'message_pwreset_success', type='info')
