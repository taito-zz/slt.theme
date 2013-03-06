from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from collective.cart.core.interfaces import IBaseAdapter
from collective.cart.shopping.interfaces import ICart
from collective.cart.shopping.interfaces import ICartAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from five import grok
from slt.content.interfaces import IMember
from slt.content.schema import IMemberArea
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import ICollapsedOnLoad
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory


PasswordResetToolMessageFactory = MessageFactory("passwordresettool")


grok.templatedir('templates')


class BaseView(grok.View):
    """Base view for SLT site."""
    grok.baseclass()
    grok.layer(ISltThemeLayer)
    grok.require('zope2.View')


class PwresetFinishView(BaseView):
    grok.context(IPloneSiteRoot)
    grok.name('pwreset_finish')

    def render(self):
        portal_url = self.context.absolute_url()
        message = PasswordResetToolMessageFactory('message_pwreset_success')
        IStatusMessage(self.request).addStatusMessage(message, type='info')
        url = '{0}/login_form?came_from={0}'.format(portal_url)
        return self.request.response.redirect(url)


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
                'shipping_method': cart.shipping_method,
                'state_title': workflow.getTitleForStateOnType(item.review_state(), item.portal_type),
                'title': item.Title(),
                'total': cart.total,
                'url': item.getURL(),
                'billing_info': cart.billing_info,
                'shipping_info': cart.shipping_info,
            })
        return res

    def class_collapsible(self):
        utility = getUtility(ICollapsedOnLoad)
        if len(self.carts) == 1:
            return utility(collapsed=False)
        return utility()
