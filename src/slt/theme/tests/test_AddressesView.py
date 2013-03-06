from slt.theme.browser.template import AddressesView
from slt.theme.tests.base import IntegrationTestCase

import mock


class AddressesViewTestCase(IntegrationTestCase):
    """TestCase for AddressesView"""

    def test_subclass(self):
        from slt.theme.browser.template import BaseMemberAreaView
        self.assertTrue(issubclass(AddressesView, BaseMemberAreaView))

    def test_name(self):
        self.assertEqual(getattr(AddressesView, 'grokcore.component.directive.name'), 'addresses')

    def test_template(self):
        self.assertEqual(getattr(AddressesView, 'grokcore.view.directive.template'), 'addresses')

    @mock.patch('slt.theme.browser.template.IMember')
    def test_addresses(self, IMember):
        instance = self.create_view(AddressesView)
        self.assertEqual(instance.addresses, IMember().infos)
