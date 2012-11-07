from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok
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


class AddressListView(BaseView):
    """View for listing addresses for MemberArea."""
    grok.context(IMemberArea)
    grok.name('addresses')
    grok.template('addresses')


class OrderListView(BaseView):
    """View for listing orders for MemberArea."""
    grok.context(IMemberArea)
    grok.name('orders')
    grok.template('orders')
