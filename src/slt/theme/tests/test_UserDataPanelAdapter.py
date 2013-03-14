from slt.theme.browser.personalpreferences import UserDataPanelAdapter
from slt.theme.tests.base import IntegrationTestCase


class UserDataPanelAdapterTestCase(IntegrationTestCase):
    """TestCase for UserDataPanelAdapter"""

    def test_set_registration_number(self):
        instance = UserDataPanelAdapter(self.portal)
        instance.set_registration_number(None)
        self.assertEqual(instance.context.registration_number, '')

    def test_set_allow_direct_marketing(self):
        instance = UserDataPanelAdapter(self.portal)
        instance.set_allow_direct_marketing(None)
        self.assertFalse(instance.context.allow_direct_marketing)
