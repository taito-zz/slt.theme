# -*- coding: utf-8 -*-
from slt.theme.browser.interfaces import IShopArticleListingViewlet
from slt.theme.browser.viewlet import ShopArticleListingViewlet
from slt.theme.tests.base import IntegrationTestCase
from zope.interface import alsoProvides
from zope.lifecycleevent import modified

import mock


class ShopArticleListingViewletTestCase(IntegrationTestCase):
    """TestCase for ShopArticleListingViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(ShopArticleListingViewlet, Base)
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IShopArticleListingViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(ShopArticleListingViewlet)
        self.assertTrue(verifyObject(IShopArticleListingViewlet, instance))

    @mock.patch('slt.theme.browser.viewlet.IArticleAdapter')
    def test_articles(self, IArticleAdapter):
        IArticleAdapter().discount_available.return_value = False
        instance = self.create_viewlet(ShopArticleListingViewlet)
        self.assertEqual(len(instance.articles()), 0)

        article1 = self.create_content('collective.cart.core.Article', title='Ärticle1', description='Descriptiön of Ärticle1',
            feed_order=2, money=self.money('12.40'), vat_rate=24.0)
        self.assertEqual(len(instance.articles()), 0)

        from slt.theme.interfaces import IFeedToShopTop
        alsoProvides(article1, IFeedToShopTop)
        modified(article1)
        self.assertEqual(len(instance.articles()), 1)

        article2 = self.create_content('collective.cart.core.Article', title='Ärticle2', description='Descriptiön of Ärticle2',
            feed_order=1, money=self.money('12.40'), vat_rate=24.0)
        alsoProvides(article2, IFeedToShopTop)
        modified(article2)
        self.assertEqual(len(instance.articles()), 2)
        self.assertEqual([article['title'] for article in instance.articles()], ['Ärticle1', 'Ärticle2'])

        article2.feed_order = 3
        modified(article2)
        self.assertEqual([article['title'] for article in instance.articles()], ['Ärticle2', 'Ärticle1'])

        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        getUtility(IRegistry)['slt.theme.articles_feed_on_top_page'] = 1
        self.assertEqual(len(instance.articles()), 1)
        self.assertEqual(instance.articles(), [{
            'class': 'normal',
            'description': 'Descriptiön of Ärticle2',
            'feed_order': 3,
            'title': 'Ärticle2',
            'url': 'http://nohost/plone/article2'
        }])

        getUtility(IRegistry)['slt.theme.articles_feed_on_top_page'] = 0
        self.assertEqual(len(instance.articles()), 2)

        IArticleAdapter().discount_available.return_value = True
        getUtility(IRegistry)['slt.theme.articles_feed_on_top_page'] = 1
        self.assertEqual(instance.articles(), [{
            'class': 'discount',
            'description': 'Descriptiön of Ärticle2',
            'feed_order': 3,
            'title': 'Ärticle2',
            'url': 'http://nohost/plone/article2'
        }])
