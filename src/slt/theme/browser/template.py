from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.cart.core.interfaces import IBaseAdapter
from collective.cart.shopping.interfaces import ICart
from collective.cart.shopping.interfaces import ICartAdapter
from five import grok
from slt.content.interfaces import IMember
from slt.content.schema import IMemberArea
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import ICollapsedOnLoad
from zope.component import getMultiAdapter
from zope.component import getUtility


grok.templatedir('templates')


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

    def carts(self):
        base = IBaseAdapter(self.context)
        res = []
        creator = getMultiAdapter((self.context, self.request), name="plone_portal_state").member().id
        workflow = getToolByName(self.context, 'portal_workflow')
        for item in base.get_content_listing(ICart, Creator=creator, path='/', sort_on="modified", sort_order="descending"):
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
        return getUtility(ICollapsedOnLoad)()
