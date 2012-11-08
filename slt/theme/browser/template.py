from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.cart.core.browser.base import BaseListingObject
from collective.cart.shopping.interfaces import ICart
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.content.schema import IMemberArea


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

    def update(self):
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)


class AddressListView(BaseListView):
    """View for listing addresses for MemberArea."""
    grok.name('addresses')
    grok.template('addresses')

    def addresses(self):
        return []


class OrderListView(BaseListView, BaseListingObject):
    """View for listing orders for MemberArea."""
    grok.name('view')
    grok.template('orders')

    def carts(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'Creator': self.context.getOwner().getId(),
            'object_provides': ICart.__identifier__,
        }
        result = []
        for item in IContentListing(catalog(query)):
            res = {
                'id': item.getId(),
                'title': item.Title(),
                'url': item.getURL(),
                'review_state': item.review_state(),
                'modified': self._localized_time(item),
            }
            result.append(res)
        return result
