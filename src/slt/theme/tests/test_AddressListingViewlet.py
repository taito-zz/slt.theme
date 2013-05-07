# -*- coding: utf-8 -*-
from slt.theme.browser.interfaces import IAddressListingViewlet
from slt.theme.browser.viewlet import AddressListingViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class AddressListingViewletTestCase(IntegrationTestCase):
    """TestCase for AddressListingViewlet"""

    def test_subclass(self):
        from plone.app.layout.viewlets.common import ViewletBase as Base
        self.assertTrue(issubclass(AddressListingViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IAddressListingViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(AddressListingViewlet)
        self.assertTrue(verifyObject(IAddressListingViewlet, instance))

    @mock.patch('slt.theme.browser.viewlet.IMember')
    def test_addresses(self, IMember):
        view = mock.Mock()
        instance = self.create_viewlet(AddressListingViewlet, view=view)
        IMember().infos.return_value = []
        self.assertEqual(len(instance.addresses()), 0)

        address1 = self.create_content('collective.cart.shopping.CustomerInfo', id='address1',
            first_name='FIRST1', last_name='LAST1', organization='ORGANIZATION1', city='CITY1', post='POST1',
            street='STREET1', email='EMAIL1', phone='PHONE1')

        IMember().infos.return_value = [address1]
        self.assertEqual(len(instance.addresses()), 1)
        self.assertEqual(instance.addresses(), [{
            'city': 'CITY1 POST1',
            'edit_url': 'http://nohost/plone/address1/edit',
            'email': 'EMAIL1',
            'name': 'FIRST1 LAST1',
            'organization': 'ORGANIZATION1',
            'phone': 'PHONE1',
            'street': 'STREET1'
        }])

    def test___name(self):
        instance = self.create_viewlet(AddressListingViewlet)
        item = mock.Mock()
        item.first_name = 'FIRST'
        item.last_name = 'LAST'
        self.assertEqual(instance._name(item), 'FIRST LAST')

    def test__organization(self):
        instance = self.create_viewlet(AddressListingViewlet)
        item = mock.Mock()
        item.organization = None
        item.vat = None
        self.assertIsNone(instance._organization(item))

        item.organization = 'ORGANIZATION'
        self.assertEqual(instance._organization(item), 'ORGANIZATION')

        item.vat = 'VAT'
        self.assertEqual(instance._organization(item), 'ORGANIZATION VAT')

    def test__city(self):
        instance = self.create_viewlet(AddressListingViewlet)
        item = mock.Mock()
        item.city = 'CITY'
        item.post = None
        self.assertEqual(instance._city(item), 'CITY')

        item.post = 'POST'
        self.assertEqual(instance._city(item), 'CITY POST')

    def test_class_collapsible(self):
        view = mock.Mock()
        instance = self.create_viewlet(AddressListingViewlet, view=view)
        view.addresses.return_value = []
        self.assertEqual(instance.class_collapsible(), 'collapsible')

        view.addresses.return_value = [mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()]
        self.assertEqual(instance.class_collapsible(), 'collapsible')

        view.addresses.return_value = [mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()]
        self.assertEqual(instance.class_collapsible(), 'collapsible collapsedOnLoad')
