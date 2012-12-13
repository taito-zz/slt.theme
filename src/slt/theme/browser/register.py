from plone.app import users
from slt.theme import _


class RegistrationForm(users.browser.register.RegistrationForm):
    """Registration form for SLT site"""

    description = _(
        u'help_registration_form',
        default=u'You need to be registered and logged in to buy products from our shopping site.')
