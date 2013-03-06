from slt.theme.browser.template import PasswordResetToolMessageFactory

import unittest


class PasswordResetToolMessageFactoryTestCase(unittest.TestCase):
    """TestCase for PasswordResetToolMessageFactory"""

    def test(self):
        from zope.i18nmessageid import MessageFactory
        self.assertIsInstance(PasswordResetToolMessageFactory, MessageFactory)
        self.assertEqual(PasswordResetToolMessageFactory._domain, 'passwordresettool')
