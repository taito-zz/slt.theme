from slt.theme.browser.template import PwresetFinishView
from slt.theme.tests.base import IntegrationTestCase

import mock


class PwresetFinishViewTestCase(IntegrationTestCase):
    """TestCase for PwresetFinishView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseView
        self.assertTrue(issubclass(PwresetFinishView, BaseView))

    def test_context(self):
        from Products.CMFPlone.interfaces import IPloneSiteRoot
        self.assertEqual(getattr(PwresetFinishView, 'grokcore.component.directive.context'), IPloneSiteRoot)

    def test_name(self):
        self.assertEqual(getattr(PwresetFinishView, 'grokcore.component.directive.name'), 'pwreset_finish')

    @mock.patch('slt.theme.browser.template.IStatusMessage')
    def test_render(self, IStatusMessage):
        instance = self.create_view(PwresetFinishView)
        instance.context.absolute_url = mock.Mock(return_value='portal_url')
        self.assertEqual(instance.render(), 'portal_url/login_form?came_from=portal_url')
        IStatusMessage().addStatusMessage.assert_called_with(u'message_pwreset_success', type='info')
