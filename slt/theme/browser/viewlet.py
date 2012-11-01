from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.cart.shopping.interfaces import IArticleAdapter
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IPortalFooter
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.registry.interfaces import IRegistry
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import IFeedToShopTop
from zope.component import getUtility
from zope.interface import Interface

grok.templatedir('viewlets')


class FooterViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(ISltThemeLayer)
    grok.name('plone.footer')
    grok.require('zope2.View')
    grok.template('footer')
    grok.viewletmanager(IPortalFooter)


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
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        query = {
            'path': '/'.join(context.getPhysicalPath()),
            'object_provides': IFeedToShopTop.__identifier__,
            'sort_limit': limit,
        }
        res = []
        for item in IContentListing(catalog(query)[:limit]):
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
