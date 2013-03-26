# -*- coding: utf-8 -*-
from slt.theme.browser.viewlet import ShopTopArticlesViewlet
from slt.theme.tests.base import IntegrationTestCase
from zope.interface import alsoProvides
from zope.lifecycleevent import modified

import mock


class ShopTopArticlesViewletTestCase(IntegrationTestCase):
    """TestCase for ShopTopArticlesViewlet"""

    def test_subclass(self):
        from slt.theme.browser.viewlet import BaseViewlet
        self.assertTrue(ShopTopArticlesViewlet, BaseViewlet)

    def test_context(self):
        from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
        self.assertEqual(getattr(ShopTopArticlesViewlet, 'grokcore.component.directive.context'), IPloneSiteRoot)

    def test_name(self):
        self.assertEqual(getattr(ShopTopArticlesViewlet, 'grokcore.component.directive.name'), 'slt.theme.shop.top.articles')

    def test_template(self):
        self.assertEqual(getattr(ShopTopArticlesViewlet, 'grokcore.view.directive.template'), 'shop-top-articles')

    def test_view(self):
        from plone.app.layout.globals.interfaces import IViewView
        self.assertEqual(getattr(ShopTopArticlesViewlet, 'grokcore.viewlet.directive.view'), IViewView)

    def test_viewletmanager(self):
        from slt.theme.browser.viewlet import ShopTopViewletManager
        self.assertEqual(getattr(ShopTopArticlesViewlet, 'grokcore.viewlet.directive.viewletmanager'), ShopTopViewletManager)

    @mock.patch('slt.theme.browser.viewlet.IArticleAdapter')
    @mock.patch('slt.theme.browser.viewlet.getMultiAdapter')
    def test_articles(self, getMultiAdapter, IArticleAdapter):
        IArticleAdapter().discount_available = False
        instance = self.create_viewlet(ShopTopArticlesViewlet)
        self.assertEqual(len(instance.articles), 0)

        article1 = self.create_content('collective.cart.core.Article', title='Ärticle1', description='Descriptiön of Ärticle1',
            feed_order=2, money=self.money('12.40'), vat_rate=self.decimal('24.00'))
        self.assertEqual(len(instance.articles), 0)

        from slt.theme.interfaces import IFeedToShopTop
        alsoProvides(article1, IFeedToShopTop)
        modified(article1)
        self.assertEqual(len(instance.articles), 1)

        article2 = self.create_content('collective.cart.core.Article', title='Ärticle2', description='Descriptiön of Ärticle2',
            feed_order=1, money=self.money('12.40'), vat_rate=self.decimal('24.00'))
        alsoProvides(article2, IFeedToShopTop)
        modified(article2)
        self.assertEqual(len(instance.articles), 2)
        self.assertEqual([article['title'] for article in instance.articles], ['Ärticle1', 'Ärticle2'])

        article2.feed_order = 3
        modified(article2)
        self.assertEqual([article['title'] for article in instance.articles], ['Ärticle2', 'Ärticle1'])

        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        getUtility(IRegistry)['slt.theme.articles_feed_on_top_page'] = 1
        self.assertEqual(len(instance.articles), 1)
        self.assertEqual(instance.articles, [{
            'class': 'normal',
            'description': 'Descriptiön of Ärticle2',
            'feed_order': 3,
            'title': 'Ärticle2',
            'url': 'http://nohost/plone/article2'
        }])

        getUtility(IRegistry)['slt.theme.articles_feed_on_top_page'] = 0
        self.assertEqual(len(instance.articles), 2)

        IArticleAdapter().discount_available = True
        getUtility(IRegistry)['slt.theme.articles_feed_on_top_page'] = 1
        self.assertEqual(instance.articles, [{
            'class': 'discount',
            'description': 'Descriptiön of Ärticle2',
            'feed_order': 3,
            'title': 'Ärticle2',
            'url': 'http://nohost/plone/article2'
        }])
