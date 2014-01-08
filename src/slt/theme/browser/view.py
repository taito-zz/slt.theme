from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from collective.base.view import BaseFormView
from collective.cart.shopping.browser.view import ToCustomerOrderMailTemplateView as BaseToCustomerOrderMailTemplateView
from collective.cart.shopping.browser.view import ToShopOrderMailTemplateView as BaseToShopOrderMailTemplateView
from datetime import datetime
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from slt.theme import _
from slt.theme.browser.interfaces import IAddressListingView
from slt.theme.browser.interfaces import IMembersView
from slt.theme.browser.interfaces import IOrderListingView
from slt.theme.browser.interfaces import IShopView
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

import csv


PasswordResetToolMessageFactory = MessageFactory("passwordresettool")


class PwresetFinishView(BrowserView):

    def __call__(self):
        portal_url = self.context.absolute_url()
        message = PasswordResetToolMessageFactory(u'message_pwreset_success')
        IStatusMessage(self.request).addStatusMessage(message, type='info')
        url = '{0}/login_form?came_from={0}'.format(portal_url)
        return self.request.response.redirect(url)


class LoginSuccessView(BrowserView):

    def __call__(self):
        url = self.context.absolute_url()
        message = PloneMessageFactory(u'Welcome! You are now logged in.')
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        member = portal_state.member()
        if not member.getProperty('fullname'):
            url = '{}/@@personal-information'.format(portal_state.portal_url())
            message = _(u'first-time-login', default=u'Please fill your personal information.')
        IStatusMessage(self.request).addStatusMessage(message, type='info')
        return self.request.response.redirect(url)


class BaseView(BaseFormView):
    """Base view"""

    def __call__(self):
        return self.template()

    def title(self):
        """Returns title of context

        :rtype: str
        """
        return self.context.Title()

    def description(self):
        """Returns description of context

        :rtype: str
        """
        return self.context.Description()


class ShopView(BaseView):
    """View for Shop top page."""
    implements(IShopView)


class MembersView(BaseView):
    """View for @@members"""
    implements(IMembersView)

    title = _(u'Members')

    def description(self):
        return _(u'members-description',
            default=u'There are ${direct_marketing_allowers} members out of ${all_members} who allows direct marketing.',
            mapping={'direct_marketing_allowers': len(self.direct_marketing_allowers()), 'all_members': len(self.all_members())})

    @memoize
    def all_members(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.searchForMembers()

    @memoize
    def direct_marketing_allowers(self):
        res = []
        for member in self.all_members():
            if member.getProperty('allow_direct_marketing'):
                res.append(member)
        return res

    @memoize_contextless
    def table_headers(self):
        """Returns headers for table

        :rtype: tuple
        """
        return (
            _(u'ID (e-mail)'),
            _(u'Name'))

    def __call__(self):
        if self.request.form.get('form.buttons.ExportDirectMarketingAllowers') is not None:
            out = StringIO()
            writer = csv.writer(out, delimiter='|', quoting=csv.QUOTE_MINIMAL)
            plone = self.context.restrictedTraverse('@@plone')
            encoding = plone.site_encoding()
            headers = [self.context.translate(header).encode(encoding) for header in self.table_headers()]
            writer.writerow(headers)

            for member in self.direct_marketing_allowers():
                writer.writerow((
                    member.getProperty('email'),
                    member.getProperty('fullname')))

            filename = 'direct-marketing-allowers-{}.csv'.format(datetime.now().isoformat())
            cd = 'attachment; filename="{}"'.format(filename)
            self.request.response.setHeader('Content-Type', 'text/csv')
            self.request.response.setHeader("Content-Disposition", cd)
            return out.getvalue()
        return self.template()


class AddressListingView(BaseView):
    """View for listing addresses for MemberArea."""
    implements(IAddressListingView)

    title = _(u'Address Linsting')
    description = _(u'Add commonly used addresses to make your order easier.')


class OrderListingView(BaseView):
    """View for listing orders for MemberArea."""
    implements(IOrderListingView)

    title = _(u'Order Linsting')


class BaseOrderMailTemplateView(object):

    def localized_birth_date(self):
        birth_date = self.items.get('birth_date')
        if birth_date:
            toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
            return toLocalizedTime(DateTime(birth_date))


class ToCustomerOrderMailTemplateView(BaseToCustomerOrderMailTemplateView, BaseOrderMailTemplateView):
    """Mail template used to send e-mail to customer"""
    template = ViewPageTemplateFile('views/order-mail-template.pt')


class ToShopOrderMailTemplateView(BaseToShopOrderMailTemplateView, BaseOrderMailTemplateView):
    """Mail template used to send email to shop"""
    template = ViewPageTemplateFile('views/order-mail-template.pt')
