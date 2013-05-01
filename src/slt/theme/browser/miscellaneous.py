from Products.Five.browser import BrowserView
from slt.content.interfaces import IArticle
from slt.theme.interfaces import IFeedToShopTop
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.lifecycleevent import modified


class Miscellaneous(BrowserView):

    def feedable_to_shop_top(self):
        return IArticle.providedBy(self.context) and not IFeedToShopTop.providedBy(self.context)

    def unfeedable_from_shop_top(self):
        return IArticle.providedBy(self.context) and IFeedToShopTop.providedBy(self.context)

    def feed_to_shop_top(self):
        alsoProvides(self.context, IFeedToShopTop)
        modified(self.context)
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def unfeed_from_shop_top(self):
        noLongerProvides(self.context, IFeedToShopTop)
        modified(self.context)
        url = self.context.absolute_url()
        return self.request.response.redirect(url)
