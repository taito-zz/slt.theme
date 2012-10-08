from plone.app.users import userdataschema
from zope.interface import Interface


class UserDataSchemaProvider(userdataschema.UserDataSchemaProvider):
    """"""

    def getSchema(self):
        """
        """
        return IUserDataSchema


class IUserDataSchema(Interface):
    """
    """

    fullname = userdataschema.IUserDataSchema.get('fullname')
    email = userdataschema.IUserDataSchema.get('email')
