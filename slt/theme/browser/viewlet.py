from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.registry.interfaces import IRegistry
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import IFeedToShopTop
from zope.component import getUtility


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
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        query = {
            'path': '/'.join(context.getPhysicalPath()),
            'object_provides': IFeedToShopTop.__identifier__,
            'sort_limit': limit,
        }
        return [{
            'description': item.Description(),
            'style': 'style',
            'title': item.Title(),
            'url': item.getURL(),
        } for item in IContentListing(catalog(query)[:limit])]
