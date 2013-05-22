# -*- coding: utf-8 -*-
from slt.theme.browser.interfaces import IMembersExportViewlet
from slt.theme.browser.viewlet import MembersExportViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class MembersExportViewletTestCase(IntegrationTestCase):
    """TestCase for MembersExportViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(MembersExportViewlet, Base)
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IMembersExportViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(MembersExportViewlet)
        self.assertTrue(verifyObject(IMembersExportViewlet, instance))

    def test_available(self):
        view = mock.Mock()
        view.direct_marketing_allowers.return_value = []
        instance = self.create_viewlet(MembersExportViewlet, view=view)
        self.assertFalse(instance.available())
