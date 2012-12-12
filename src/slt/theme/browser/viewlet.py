from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.cart import shopping
from collective.cart.shopping.interfaces import IArticleAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.registry.interfaces import IRegistry
from slt.content.interfaces import ICartAdapter
from slt.content.interfaces import ICustomerInfoBrain
from slt.content.interfaces import IMember
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import IFeedToShopTop
from slt.theme.interfaces import ICollapsedOnLoad
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface


grok.templatedir('viewlets')


class ShopTopViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager for shop top page."""
    grok.context(IPloneSiteRoot)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.shop.top.viewletmanager')


class ShopTopArticlesViewlet(grok.Viewlet):
    """Viewlet to show articles."""
    grok.context(IPloneSiteRoot)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.shop.top.articles')
    grok.require('zope2.View')
    grok.template('shop-top-articles')
    grok.view(IViewView)
    grok.viewletmanager(ShopTopViewletManager)

    def articles(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = {
            'path': '/'.join(context.getPhysicalPath()),
            'object_provides': IFeedToShopTop.__identifier__,
        }
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        if limit:
            query['sort_limit'] = limit
            listing = IContentListing(catalog(query)[:limit])
        else:
            listing = IContentListing(catalog(query))
        res = []
        for item in listing:
            style_class = 'normal'
            if IArticleAdapter(item.getObject()).discount_available:
                style_class = 'discount'
            res.append({
                'description': item.Description(),
                'class': style_class,
                'title': item.Title(),
                'url': item.getURL(),
            })
        return res


class AddressesViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager for listing addresses."""
    grok.context(Interface)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.addresses.viewletmanager')


class AssressViewlet(grok.Viewlet):
    """Viewlet to show address."""
    grok.context(Interface)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.address')
    grok.require('zope2.View')
    grok.template('address')
    grok.viewletmanager(AddressesViewletManager)

    def addresses(self):
        result = []
        for item in IContentListing(self.view.addresses):
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
        return u'{} {}'.format(item.first_name, item.last_name)

    def _organization(self, item):
        org = item.organization
        if org:
            if item.vat:
                org = u'{} {}'.format(item.organization, item.vat)
            return org.strip()

    def _city(self, item):
        if item.post:
            city = u'{} {}'.format(item.city, item.post)
            return city.strip()

    def class_collapsible(self):
        return getUtility(ICollapsedOnLoad)(len(self.view.addresses) > 4)


class BaseCustomerInfoViewlet(grok.Viewlet):
    grok.baseclass()

    def update(self):
        form = self.request.form
        uuid = form.get(self.button)
        if uuid is not None:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(UID=uuid)
            if brains:
                cart = shopping.interfaces.IShoppingSite(self.context).cart
                ICartAdapter(cart).update_address(self._name, brains[0])
                url = getMultiAdapter(
                    (self.context, self.request), name='plone_context_state').current_base_url()
                self.request.response.redirect(url)

    def get_address(self, name):
        cart = shopping.interfaces.IShoppingSite(self.context).cart
        address = ICartAdapter(cart).get_address(name)

        if address:
            return ICustomerInfoBrain(address)()

    @property
    def address(self):
        return self.get_address(self._name)

    def addresses(self):
        if self.address:
            res = []
            for brain in IMember(self.context).rest_of_infos(self.address['orig_uuid']):
                res.append(ICustomerInfoBrain(brain)())
            return res

    def class_collapsible_address(self):
        if self.address:
            return getUtility(ICollapsedOnLoad)(False)

    def class_collapsed(self):
        return getUtility(ICollapsedOnLoad)()

    def class_collapsible_form(self):
        return getUtility(ICollapsedOnLoad)(self.address)

    @property
    def button(self):
        return 'form.buttons.Change{}Address'.format(self._name.capitalize())


class BillingInfoViewlet(shopping.browser.viewlet.BillingInfoViewlet, BaseCustomerInfoViewlet):
    grok.layer(ISltThemeLayer)

    _name = 'billing'


class ShippingInfoViewlet(shopping.browser.viewlet.ShippingInfoViewlet, BaseCustomerInfoViewlet):
    grok.layer(ISltThemeLayer)

    _name = 'shipping'


class CheckOutViewlet(shopping.browser.viewlet.CheckOutViewlet):
    """Viewlet to display check out buttons."""
    grok.layer(ISltThemeLayer)

    def update(self):
        form = self.request.form
        if form.get('form.checkout') is not None:
            cart = IShoppingSite(self.context).cart
            # Update addresses.
            ICartAdapter(cart).add_addresses()
        super(CheckOutViewlet, self).update()
