from plone.app.users.browser import personalpreferences
from slt.theme.userdataschema import IUserDataSchema
from zope.formlib import form


class UserDataPanel(personalpreferences.UserDataPanel):

    def __init__(self, context, request):
        super(
            personalpreferences.UserDataPanel, self).__init__(context, request)
        self.form_fields = form.FormFields(IUserDataSchema)
