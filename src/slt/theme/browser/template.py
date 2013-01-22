from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from Products.validation import validation
from collective.cart.core.interfaces import IBaseAdapter
from collective.cart.shopping.browser.base import Message
from collective.cart.shopping.browser.template import BaseCheckoutView
from collective.cart.shopping.interfaces import ICart
from collective.cart.shopping.interfaces import ICartAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from five import grok
from plone.dexterity.utils import createContentInContainer
from slt.content.interfaces import IMember
from slt.content.schema import IMemberArea
from slt.theme import _
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import ICollapsedOnLoad
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.lifecycleevent import modified


grok.templatedir('templates')


class BillingInfoView(BaseCheckoutView, Message):
    """View for editing billing info which checkout"""
    grok.name('billing-info')
    grok.template('billing-info')

    def billing_info(self):
        shopping_site = IShoppingSite(self.context)
        cart = shopping_site.cart
        billing = cart.get('billing')
        if billing:
            return {
                'first_name': billing.first_name,
                'last_name': billing.last_name,
                'organization': billing.organization,
                'vat': billing.vat,
                'email': billing.email,
                'street': billing.street,
                'post': billing.post,
                'city': billing.city,
                'phone': billing.phone,
            }
        else:
            return {
                'first_name': '',
                'last_name': '',
                'organization': '',
                'vat': '',
                'email': '',
                'street': '',
                'post': '',
                'city': '',
                'phone': '',
            }

    def update(self):
        form = self.request.form
        shopping_site = IShoppingSite(self.context)
        shop_url = shopping_site.shop.absolute_url()
        if form.get('form.buttons.back') is not None:
            IShoppingSite(self.context).shop
            url = '{}/@@billing-and-shipping'.format(shop_url)
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

                billing = cart.get('billing')
                if billing is None:
                    billing = createContentInContainer(
                        cart, 'collective.cart.shopping.CustomerInfo', id='billing',
                        checkConstraints=False, **data)
                else:
                    for key in data:
                        if getattr(billing, key) != data[key]:
                            setattr(billing, key, data[key])

                modified(billing)
                url = '{}/@@order-confirmation'.format(shop_url)
                return self.request.response.redirect(url)


class BaseView(grok.View):
    """Base view for SLT site."""
    grok.baseclass()
    grok.layer(ISltThemeLayer)
    grok.require('zope2.View')


class ShopView(BaseView):
    """View for Shop top page."""
    grok.context(IPloneSiteRoot)
    grok.name('slt-view')
    grok.template('shop')


class BaseListView(BaseView):
    """Base view for listing for MemberArea."""
    grok.baseclass()
    grok.context(IMemberArea)


class AddressListView(BaseListView):
    """View for listing addresses for MemberArea."""
    grok.name('addresses')
    grok.template('addresses')

    @property
    def addresses(self):
        return IMember(self.context).infos


class OrderListView(BaseListView):
    """View for listing orders for MemberArea."""
    grok.name('view')
    grok.template('orders')

    @property
    def carts(self):
        base = IBaseAdapter(self.context)
        res = []
        creator = getMultiAdapter((self.context, self.request), name="plone_portal_state").member().id
        workflow = getToolByName(self.context, 'portal_workflow')
        shop = IShoppingSite(self.context).shop
        query = {
            'Creator': creator,
            'path': '/'.join(shop.getPhysicalPath()),
            'sort_on': 'modified',
            'sort_order': 'descending',
        }
        order_number = self.request.form.get('order_number')
        if order_number:
            query['id'] = order_number
        for item in base.get_content_listing(ICart, **query):
            obj = item.getObject()
            cart = ICartAdapter(obj)
            res.append({
                'articles': cart.articles,
                'id': item.getId(),
                'modified': base.localized_time(item),
                'state_title': workflow.getTitleForStateOnType(item.review_state(), item.portal_type),
                'title': item.Title(),
                'total': cart.total,
                'url': item.getURL(),
            })
        return res

    def class_collapsible(self):
        utility = getUtility(ICollapsedOnLoad)
        if len(self.carts) == 1:
            return utility(collapsed=False)
        return utility()
