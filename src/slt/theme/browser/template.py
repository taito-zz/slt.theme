from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.base.view import BaseFormView
from collective.cart.shopping.browser.template import ToCustomerOrderMailTemplateView as BaseToCustomerOrderMailTemplateView
from collective.cart.shopping.browser.template import ToShopOrderMailTemplateView as BaseToShopOrderMailTemplateView
from slt.theme import _
from slt.theme.browser.interfaces import IAddressListingView
from slt.theme.browser.interfaces import IOrderListingView
from slt.theme.browser.interfaces import IShopView
from zope.i18nmessageid import MessageFactory
from zope.interface import implements


PasswordResetToolMessageFactory = MessageFactory("passwordresettool")


class PwresetFinishView(BrowserView):

    def __call__(self):
        portal_url = self.context.absolute_url()
        message = PasswordResetToolMessageFactory(u'message_pwreset_success')
        IStatusMessage(self.request).addStatusMessage(message, type='info')
        url = '{0}/login_form?came_from={0}'.format(portal_url)
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


class AddressListingView(BaseView):
    """View for listing addresses for MemberArea."""
    implements(IAddressListingView)

    title = _(u'Address Linsting')
    description = None


class OrderListingView(BaseView):
    """View for listing orders for MemberArea."""
    implements(IOrderListingView)

    title = _(u'Order Linsting')
    description = _(u'Add commonly used addresses to make your order easier.')


class ToCustomerOrderMailTemplateView(BaseToCustomerOrderMailTemplateView):
    """Mail template used to send e-mail to customer"""
    template = ViewPageTemplateFile('templates/order-mail-template.pt')


class ToShopOrderMailTemplateView(BaseToShopOrderMailTemplateView):
    """Mail template used to send email to shop"""
    template = ViewPageTemplateFile('templates/order-mail-template.pt')
