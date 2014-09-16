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

    def test_set_birth_date(self):
        member = self.portal.portal_membership.getAuthenticatedMember()
        member.setMemberProperties({'birth_date': '20.01.1990'})
        self.assertEqual(member.getProperty('birth_date'), '20.01.1990')
        instance = UserDataPanelAdapter(self.portal)
        instance.set_birth_date()
        self.assertEqual(member.getProperty('birth_date'), '')
