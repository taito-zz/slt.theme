from plone.app.users.browser import personalpreferences
from slt.theme.userdataschema import IUserDataSchema
from zope.formlib import form


class UserDataPanel(personalpreferences.UserDataPanel):

    def __init__(self, context, request):
        super(personalpreferences.UserDataPanel, self).__init__(context, request)
        self.form_fields = form.FormFields(IUserDataSchema)


class UserDataPanelAdapter(personalpreferences.UserDataPanelAdapter):

    def get_registration_number(self):
        return self._getProperty('registration_number')

    def set_registration_number(self, value):
        if value is None:
            value = ''
        return self.context.setMemberProperties({'registration_number': value})

    registration_number = property(get_registration_number, set_registration_number)

    def get_allow_direct_marketing(self):
        return self._getProperty('allow_direct_marketing')

    def set_allow_direct_marketing(self, value):
        if value is None:
            value = False
        return self.context.setMemberProperties({'allow_direct_marketing': value})

    allow_direct_marketing = property(get_allow_direct_marketing, set_allow_direct_marketing)
