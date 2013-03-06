from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from collective.cart.shopping.interfaces import ICart
from collective.cart.shopping.interfaces import ICartAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from five import grok
from plone.memoize.view import memoize
from slt.content.interfaces import IMember
from slt.content.schema import IMemberArea
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import ICollapsedOnLoad
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

    @memoize
    def render(self):
        portal_url = self.context.absolute_url()
        message = PasswordResetToolMessageFactory(u'message_pwreset_success')
        IStatusMessage(self.request).addStatusMessage(message, type='info')
        url = '{0}/login_form?came_from={0}'.format(portal_url)
        return self.request.response.redirect(url)


class ShopView(BaseView):
    """View for Shop top page."""
    grok.context(IPloneSiteRoot)
    grok.name('slt-view')
    grok.template('shop')


class BaseMemberAreaView(BaseView):
    """Base view for MemberArea."""
    grok.baseclass()
    grok.context(IMemberArea)


class AddressesView(BaseMemberAreaView):
    """View for listing addresses for MemberArea."""
    grok.name('addresses')
    grok.template('addresses')

    @property
    def addresses(self):
        return IMember(self.context).infos


class OrdersView(BaseMemberAreaView):
    """View for listing orders for MemberArea."""
    grok.name('view')
    grok.template('orders')

    @property
    def carts(self):
        shopping_site = IShoppingSite(self.context)
        res = []
        creator = getToolByName(self.context, 'portal_membership').getAuthenticatedMember().id
        workflow = getToolByName(self.context, 'portal_workflow')
        query = {
            'Creator': creator,
            'path': shopping_site.shop_path,
            'sort_on': 'modified',
            'sort_order': 'descending',
        }
        order_number = self.request.form.get('order_number')
        if order_number:
            query['id'] = order_number
        for item in shopping_site.get_content_listing(ICart, **query):
            obj = item.getObject()
            cart = ICartAdapter(obj)
            res.append({
                'articles': cart.articles,
                'id': item.getId(),
                'modified': shopping_site.ulocalized_time(item.modified),
                'shipping_method': cart.shipping_method,
                'state_title': workflow.getTitleForStateOnType(item.review_state(), item.portal_type),
                'title': item.Title(),
                'total': cart.total,
                'url': item.getURL(),
                'billing_info': cart.get_address('billing'),
                'shipping_info': cart.get_address('shipping'),
            })
        return res

    @property
    def class_collapsible(self):
        utility = getUtility(ICollapsedOnLoad)
        if len(self.carts) == 1:
            return utility(collapsed=False)
        return utility()
