from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok
from slt.theme.browser.interfaces import ISltThemeLayer


grok.templatedir('templates')


class ShopView(grok.View):

    grok.context(IPloneSiteRoot)
    grok.layer(ISltThemeLayer)
    grok.name('slt-view')
    grok.require('zope2.View')
    grok.template('shop')
