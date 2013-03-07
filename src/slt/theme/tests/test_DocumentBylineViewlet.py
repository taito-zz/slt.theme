from slt.theme.browser.viewlet import DocumentBylineViewlet
from slt.theme.tests.base import IntegrationTestCase


class DocumentBylineViewletTestCase(IntegrationTestCase):
    """TestCase for DocumentBylineViewlet"""

    def test_subclass(self):
        from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet
        self.assertTrue(issubclass(DocumentBylineViewlet, BaseDocumentBylineViewlet))

    def test_show(self):
        instance = self.create_viewlet(DocumentBylineViewlet)
        self.assertTrue(instance.show())
