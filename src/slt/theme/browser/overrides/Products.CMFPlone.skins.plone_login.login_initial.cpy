## Controller Python Script "login_initial"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Handle a user's initial login
##

# do anything that must be done during a user's initial login here

from Products.CMFPlone import PloneMessageFactory as _

util = context.plone_utils
util.addPortalMessage(_(u'first-time-login', default=u'Please fill your personal information.'), 'info')
url = '{}/@@personal-information'.format(context.portal_url())

return context.REQUEST.RESPONSE.redirect(url)

# afterwards, change the password if necessary
if state.getKwargs().get('must_change_password',0):
    state.set(status='login_change_password')
return state
