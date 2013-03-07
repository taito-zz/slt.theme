from slt.theme.userdataschema import UserDataSchemaProvider

import unittest


class UserDataSchemaProviderTestCase(unittest.TestCase):
    """TestCase for UserDataSchemaProvider"""

    def test_subclass(self):
        from plone.app.users.userdataschema import UserDataSchemaProvider as BaseUserDataSchemaProvider
        self.assertTrue(issubclass(UserDataSchemaProvider, BaseUserDataSchemaProvider))

    def test_getSchema(self):
        from slt.theme.userdataschema import IUserDataSchema
        instance = UserDataSchemaProvider()
        self.assertEqual(instance.getSchema(), IUserDataSchema)
