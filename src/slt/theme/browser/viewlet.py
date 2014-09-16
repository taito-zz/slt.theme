from DateTime import DateTime
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.base.viewlet import Viewlet
from collective.cart.shopping.browser.viewlet import BillingAndShippingBillingAddressViewlet as BaseBillingAndShippingBillingAddressViewlet
from collective.cart.shopping.interfaces import IShoppingSite
from datetime import date
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet
from plone.memoize import ram
from plone.memoize import view
from plone.registry.interfaces import IRegistry
from slt.content.interfaces import IMember
from slt.theme.browser.interfaces import IAddAddressViewlet
from slt.theme.browser.interfaces import IAddressListingViewlet
from slt.theme.browser.interfaces import IBillingAndShippingBillingAddressViewlet
from slt.theme.browser.interfaces import ILinkToOrderViewlet
from slt.theme.browser.interfaces import IMembersExportViewlet
from slt.theme.browser.interfaces import IOrderListingBirthDateViewlet
from slt.theme.browser.interfaces import IOrderListingRegistrationNumberViewlet
from slt.theme.browser.interfaces import IShopArticleListingViewlet
from slt.theme.interfaces import ICollapsedOnLoad
from slt.theme.interfaces import IFeedToShopTop
from zope.annotation.interfaces import IAnnotations
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


def _objs_p_mtime_cachekey(method, self):
    return IAnnotations(self.context).get('_objs_p_mtime')


class ShopArticleListingViewlet(Viewlet):
    """Viewlet for view: @@slt-view
    Shows article listing
    """
    implements(IShopArticleListingViewlet)
    index = ViewPageTemplateFile('viewlets/shop-article-listing.pt')

    def update(self):
        super(ShopArticleListingViewlet, self).update()
        annotations = IAnnotations(self.context)
        current_objs_p_mtime = annotations.get('_objs_p_mtime')
        objs_p_mtime = [obj.image._p_mtime for obj in self._objs()]
        if current_objs_p_mtime != objs_p_mtime:
            annotations['_objs_p_mtime'] = objs_p_mtime

    def _objs(self):
        """Returns list of article objects

        :rtype: list
        """
        query = {
            'sort_on': 'feed_order',
            'sort_order': 'descending',
        }
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        if limit:
            query['sort_limit'] = limit
        return IShoppingSite(self.context).get_objects(IFeedToShopTop, **query)

    @ram.cache(_objs_p_mtime_cachekey)
    def articles(self):
        """Returns content listing
        """
        return IContentListing(self._objs())

    @ram.cache(_objs_p_mtime_cachekey)
    def number_of_articles(self):
        """Return number of articles"""
        return len(self.articles())


class MembersExportViewlet(Viewlet):
    """Viewlet for view: @@members

    Shows member export buttons
    """
    implements(IMembersExportViewlet)
    index = ViewPageTemplateFile('viewlets/members-export.pt')

    def available(self):
        if self.view.direct_marketing_allowers():
            return True
        return False


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
        return getUtility(ICollapsedOnLoad)(len(self.addresses()) > 4)


class BillingAndShippingBillingAddressViewlet(BaseBillingAndShippingBillingAddressViewlet):
    """Viewlet class to show form to update billing address"""
    implements(IBillingAndShippingBillingAddressViewlet)
    index = ViewPageTemplateFile('viewlets/billing-and-shipping-billing-address.pt')

    @view.memoize
    def today(self):
        """Today"""
        return date.today()

    def localized_today(self):
        """Localized today"""
        toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
        return toLocalizedTime(DateTime(self.today().isoformat()))

    def birth_date(self):
        """Return birth date

        :rtype: str
        """
        return self.view.shopping_site().cart().get('birth_date') or self.context.restrictedTraverse(
            '@@plone_portal_state').member().getProperty('birth_date', None)

    def localized_birth_date(self):
        birth_date = self.birth_date()
        if birth_date:
            toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
            return toLocalizedTime(DateTime(self.birth_date()))

    def registration_number(self):
        """Returns registration number

        :rtype: str
        """
        return self.view.shopping_site().cart().get('registration_number') or self.context.restrictedTraverse(
            '@@plone_portal_state').member().getProperty('registration_number')

    def update(self):
        form = self.request.form
        registration_number = form.get('registration_number')
        if form.get('form.buttons.CheckOut') is not None:
            if registration_number is not None:
                self.view.shopping_site().update_cart('registration_number', registration_number.strip())


class OrderListingRegistrationNumberViewlet(Viewlet):
    """Viewlet for order listing to show registration number"""
    implements(IOrderListingRegistrationNumberViewlet)
    index = ViewPageTemplateFile('viewlets/order-listing-registration-number.pt')

    def _handle_repeated(self, item):
        self.registration_number = getattr(item['obj'], 'registration_number', None)


class OrderListingBirthDateViewlet(Viewlet):
    """Viewlet for order listing to show birth date"""
    implements(IOrderListingBirthDateViewlet)
    index = ViewPageTemplateFile('viewlets/order-listing-birth-date.pt')

    def _handle_repeated(self, item):
        birth_date = getattr(item['obj'], 'birth_date', None)
        if birth_date is not None:
            toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
            birth_date = toLocalizedTime(DateTime(birth_date))
        self.birth_date = birth_date
