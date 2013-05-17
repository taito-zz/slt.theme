from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.base.viewlet import Viewlet
from collective.cart.shopping.interfaces import IArticleAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet
from plone.registry.interfaces import IRegistry
from slt.content.interfaces import IMember
from slt.theme.browser.interfaces import IAddAddressViewlet
from slt.theme.browser.interfaces import IAddressListingViewlet
from slt.theme.browser.interfaces import IBillingAndShippingRegistrationNumberViewlet
from slt.theme.browser.interfaces import ILinkToOrderViewlet
# from slt.theme.browser.interfaces import IOrderConfirmationRegistrationNumberViewlet
from slt.theme.browser.interfaces import IOrderListingRegistrationNumberViewlet
from slt.theme.browser.interfaces import IShopArticleListingViewlet
from slt.theme.interfaces import ICollapsedOnLoad
from slt.theme.interfaces import IFeedToShopTop
from zope.component import getUtility
from zope.interface import implements


class DocumentBylineViewlet(BaseDocumentBylineViewlet):
    """Global viewlet
    Shows document byline only for roles: Site Admin and Manager
    """

    def show(self):
        if _checkPermission('slt.theme: Show byline', self.context):
            return True


class LinkToOrderViewlet(Viewlet):
    """Viewlet for view: @@thanks
    Shows link to order
    """
    implements(ILinkToOrderViewlet)
    index = ViewPageTemplateFile('viewlets/link-to-order.pt')

    def order_url(self):
        """Returns URL for order

        :rtype: str
        """
        membership = getToolByName(self.context, 'portal_membership')
        return '{}?order_number={}'.format(membership.getHomeUrl(), self.view.order_id)


class ShopArticleListingViewlet(Viewlet):
    """Viewlet for view: @@slt-view
    Shows article listing"""
    implements(IShopArticleListingViewlet)
    index = ViewPageTemplateFile('viewlets/shop-article-listing.pt')

    def articles(self):
        """Returns list of dictionary of articles

        :rtype: list
        """
        query = {
            'sort_on': 'feed_order',
            'sort_order': 'descending',
        }
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        if limit:
            query['sort_limit'] = limit
        res = []
        context_state = self.context.restrictedTraverse('@@plone_context_state')
        for item in IShoppingSite(self.context).get_content_listing(IFeedToShopTop, **query):
            style_class = 'normal'
            if IArticleAdapter(item.getObject()).discount_available():
                style_class = 'discount'
            res.append({
                'description': item.Description(),
                'class': style_class,
                'feed_order': context_state.is_editable() and item.feed_order,
                'title': item.Title(),
                'url': item.getURL(),
            })
        return res


class AddAddressViewlet(Viewlet):
    """Viewlet for view: @@address-listing
    Shows button to add new address"""
    implements(IAddAddressViewlet)
    index = ViewPageTemplateFile('viewlets/add-address.pt')


class AddressListingViewlet(Viewlet):
    """Viewlet for view: @@address-listing
    Shows address listing"""
    implements(IAddressListingViewlet)
    index = ViewPageTemplateFile('viewlets/address-listing.pt')

    def addresses(self):
        result = []
        for item in IContentListing(IMember(self.context).infos()):
            res = {
                'name': self._name(item),
                'organization': self._organization(item),
                'street': item.street,
                'city': self._city(item),
                'email': item.email,
                'phone': item.phone,
                'edit_url': '{}/edit'.format(item.getURL()),
            }
            result.append(res)
        return result

    def _name(self, item):
        return '{} {}'.format(item.first_name, item.last_name).strip()

    def _organization(self, item):
        org = item.organization
        if org:
            if item.vat:
                org = '{} {}'.format(item.organization, item.vat)
            return org.strip()

    def _city(self, item):
        city = item.city
        if item.post:
            city = '{} {}'.format(city, item.post)
        return city.strip()

    def class_collapsible(self):
        return getUtility(ICollapsedOnLoad)(len(self.view.addresses()) > 4)


class BillingAndShippingRegistrationNumberViewlet(Viewlet):
    """Viewlet for view: @@billing-and-shipping
    Shows form to update billing address"""
    implements(IBillingAndShippingRegistrationNumberViewlet)
    index = ViewPageTemplateFile('viewlets/billing-and-shipping-registration-number.pt')

    def registration_number(self):
        """Returns registration number

        :rtype: str
        """
        return IShoppingSite(self.context).cart().get('registration_number') or self.context.restrictedTraverse(
            '@@plone_portal_state').member().getProperty('registration_number')

    def update(self):
        form = self.request.form
        registration_number = form.get('registration_number')
        if form.get('form.buttons.CheckOut') is not None and registration_number is not None:
            IShoppingSite(self.context).update_cart('registration_number', registration_number.strip())


# class OrderConfirmationRegistrationNumberViewlet(Viewlet):
#     """Viewlet for view: @@order-confirmation
#     Shows registration number"""
#     implements(IOrderConfirmationRegistrationNumberViewlet)
#     index = ViewPageTemplateFile('viewlets/order-confirmation-registration-number.pt')

#     def registration_number(self):
#         """Returns registration number

#         :rtype: str
#         """
#         cart = IShoppingSite(self.context).cart()
#         if cart:
#             return cart.get('registration_number')


class OrderListingRegistrationNumberViewlet(Viewlet):
    """Viewlet for order listing to show addresses"""
    implements(IOrderListingRegistrationNumberViewlet)
    index = ViewPageTemplateFile('viewlets/order-listing-registration-number.pt')

    def _handle_repeated(self, item):
        self.registration_number = item['obj'].registration_number
