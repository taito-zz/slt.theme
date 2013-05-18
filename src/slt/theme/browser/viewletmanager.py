from collective.cart.shopping.interfaces import IShoppingSite
from collective.cart.shopping.browser.viewletmanager import OrderListingViewletManager as BaseOrderListingViewletManager
from slt.content.interfaces import IOrder


class OrderListingViewletManager(BaseOrderListingViewletManager):
    """Viewlet manager for order listing"""

    def _orders(self):
        shopping_site = IShoppingSite(self.context)
        creator = self.context.restrictedTraverse('@@plone_portal_state').member().id
        query = {
            'Creator': creator,
            'path': shopping_site.shop_path(),
            'sort_on': 'modified',
            'sort_order': 'descending',
        }
        order_number = self.request.form.get('order_number')

        if order_number:
            query['id'] = order_number

        return shopping_site.get_content_listing(IOrder, **query)
