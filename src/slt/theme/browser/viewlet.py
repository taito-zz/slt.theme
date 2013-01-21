from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from Products.validation import validation
from collective.cart import shopping
from collective.cart.core.interfaces import IBaseAdapter
from collective.cart.shipping.interfaces import IShippingMethod
from collective.cart.shopping.browser.viewlet import BillingAndShippingViewletManager
from collective.cart.shopping.interfaces import IArticleAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.dexterity.utils import createContentInContainer
from plone.registry.interfaces import IRegistry
from slt.content.interfaces import ICartAdapter
from slt.content.interfaces import ICustomerInfoBrain
from slt.content.interfaces import IMember
from slt.theme import _
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import ICollapsedOnLoad
from slt.theme.interfaces import IFeedToShopTop
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface
from zope.lifecycleevent import modified


grok.templatedir('viewlets')


class BaseViewlet(grok.Viewlet):
    """Base class for all the viewlet"""
    grok.baseclass()
    grok.layer(ISltThemeLayer)
    grok.require('zope2.View')


class ShopTopViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager for shop top page."""
    grok.context(IPloneSiteRoot)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.shop.top.viewletmanager')


class ShopTopArticlesViewlet(BaseViewlet):
    """Viewlet to show articles."""
    grok.context(IPloneSiteRoot)
    grok.name('slt.theme.shop.top.articles')
    grok.template('shop-top-articles')
    grok.view(IViewView)
    grok.viewletmanager(ShopTopViewletManager)

    def articles(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = {
            'path': '/'.join(context.getPhysicalPath()),
            'object_provides': IFeedToShopTop.__identifier__,
            'sort_on': 'feed_order',
            'sort_order': 'descending',
        }
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        if limit:
            query['sort_limit'] = limit
            listing = IContentListing(catalog(query)[:limit])
        else:
            listing = IContentListing(catalog(query))
        res = []
        context_state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        for item in listing:
            style_class = 'normal'
            if IArticleAdapter(item.getObject()).discount_available:
                style_class = 'discount'
            res.append({
                'description': item.Description(),
                'class': style_class,
                'feed_order': context_state.is_editable() and item.feed_order,
                'title': item.Title(),
                'url': item.getURL(),
            })
        return res


class AddressesViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager for listing addresses."""
    grok.context(Interface)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.addresses.viewletmanager')


class AssressViewlet(BaseViewlet):
    """Viewlet to show address."""
    grok.context(Interface)
    grok.name('slt.theme.address')
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


# class BillingInfoViewlet(shopping.browser.viewlet.BillingInfoViewlet, BaseCustomerInfoViewlet):
#     grok.layer(ISltThemeLayer)

#     _name = 'billing'


# class ShippingInfoViewlet(shopping.browser.viewlet.ShippingInfoViewlet, BaseCustomerInfoViewlet):
#     grok.layer(ISltThemeLayer)

#     _name = 'shipping'

class ShippingInfoViewlet(BaseViewlet):
    """Viewlet class to show form to update shipping address"""
    grok.context(IPloneSiteRoot)
    grok.layer(ISltThemeLayer)
    grok.name('slt.theme.shipping.info')
    grok.template('shipping-info')
    grok.viewletmanager(BillingAndShippingViewletManager)

    # def shipping_info(self):
    #     shopping_site = IShoppingSite(self.context)
    #     cart = shopping_site.cart
    #     shipping = cart.get('shipping')
    #     if shipping:
    #         return

    @property
    def shipping_methods(self):
        base = IBaseAdapter(self.context)
        brains = base.get_brains(IShippingMethod)
        shopping_site = IShoppingSite(self.context)
        cart = ICartAdapter(shopping_site.cart)
        res = []
        for brain in brains:
            uuid = brain.UID
            orig_uuid = cart.shipping_method.orig_uuid
            if uuid == orig_uuid:
                shipping_gross_money = cart.shipping_gross_money
            else:
                shipping_gross_money = shopping_site.get_shipping_gross_money(uuid)
            res.append({
                'description': brain.Description,
                'checked': uuid == orig_uuid,
                'title': '{}  {} {}'.format(brain.Title, shipping_gross_money.amount, shipping_gross_money.currency),
                'uuid': uuid,
            })
        return res

    @property
    def single_shipping_method(self):
        return len(self.shipping_methods) == 1

    def update(self):
        form = self.request.form
        shopping_site = IShoppingSite(self.context)
        shop_url = shopping_site.shop.absolute_url()
        if form.get('form.buttons.back') is not None:
            IShoppingSite(self.context).shop
            url = '{}/@@cart'.format(shop_url)
            return self.request.response.redirect(url)
        if form.get('form.to.confirmation') is not None:
            current_url = self.context.restrictedTraverse('@@plone_context_state').current_base_url()
            first_name = form.get('first-name')
            if not first_name:
                message = _('First name is missing.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)
            last_name = form.get('last-name')
            if not last_name:
                message = _('Last name is missing.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)
            email = form.get('email')
            email_validation = validation.validatorFor('isEmail')
            if email_validation(email) != 1:
                message = _('Invalid e-mail address.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)
            street = form.get('street')
            if not street:
                message = _('Street address is missing.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)
            city = form.get('city')
            if not city:
                message = _('City is missing.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)
            phone = form.get('phone')
            if not phone:
                message = _('Phone number is missing.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)
            shipping_method = form.get('shipping-method')
            if not self.single_shipping_method and not shipping_method:
                message = _('Select one shipping method.')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return self.request.response.redirect(current_url)

            else:
                organization = form.get('organization')
                vat = form.get('vat')
                post = form.get('post')

                cart = shopping_site.cart

                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'organization': organization,
                    'vat': vat,
                    'email': email,
                    'street': street,
                    'post': post,
                    'city': city,
                    'phone': phone,
                }

                shipping = cart.get('shipping')
                if shipping is None:
                    shipping = createContentInContainer(
                        cart, 'collective.cart.shopping.CustomerInfo', id='shipping',
                        checkConstraints=False, **data)
                else:
                    for key in data:
                        if getattr(shipping, key) != data[key]:
                            setattr(shipping, key, data[key])

                modified(shipping)

                if form.get('billing-same-as-shipping') == 'same':
                    cart.billing_same_as_shipping = True
                    url = '{}/@@order-confirmation'.format(shop_url)
                    # return self.request.response.redirect(url)
                else:
                    url = '{}/@@billing-info'.format(shop_url)

                return self.request.response.redirect(url)
                    # billing = cart.get('billing')
                    # if billing is None:
                    #     billing = createContentInContainer(
                    #         cart, 'collective.cart.shopping.CustomerInfo', id='billing',
                    #         checkConstraints=False, **data)
                    # else:
                    #     for key in data:
                    #         if getattr(billing, key) != data[key]:
                    #             setattr(billing, key, data[key])

                    # modified(billing)


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
