from plone.app.users import userdataschema
from slt.theme import _
from zope import schema
from zope.interface import Interface


# class UserDataSchemaProvider(userdataschema.UserDataSchemaProvider):
#     """"""

#     def getSchema(self):
#         """
#         """
#         return IUserDataSchema


class IUserDataSchema(Interface):
    """
    """

    fullname = userdataschema.IUserDataSchema.get('fullname')
    email = userdataschema.IUserDataSchema.get('email')

    registration_number = schema.TextLine(
        title=_('Registration Number'),
        required=False)
