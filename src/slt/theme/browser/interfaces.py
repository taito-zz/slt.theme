from collective.base.interfaces import IBaseFormView
from collective.base.interfaces import IViewlet
from sll.basetheme.browser.interfaces import INavigationRootView
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


# Browser layer

class ISltThemeLayer(Interface):
    """Marker interface for browserlayer."""


# Viewlet manager

class IBaseViewViewletManager(IViewletManager):
    """Viewlet manager interface for base view"""


# View

class IShopView(IBaseFormView, INavigationRootView):
    """View interface for ShopView"""


class IAddressListingView(IBaseFormView):
    """View interface for AddressListingView"""


class IOrderListingView(IBaseFormView):
    """View interface for OrderListingView"""


# Viewlet

class ILinkToOrderViewlet(IViewlet):
    """Viewlet interface for LinkToOrderViewlet"""

    def order_url():
        """Returns URL for order

        :rtype: str
        """


class IShopArticleListingViewlet(IViewlet):
    """Viewlet interface for ShopArticleListingViewlet"""

    def articles():
        """Returns list of dictionary of articles

        :rtype: list
        """


class IAddAddressViewlet(IViewlet):
    """Viewlet interface for AddAddressViewlet"""


class IAddressListingViewlet(IViewlet):
    """Viewlet interface for AddressListingViewlet"""

    def addresses():
        """Returns list of dictionary of addresses

        :rtype: list
        """

    def class_collapsible():
        """Returns class for styling

        :rtype: str
        """


class IOrderListingViewlet(IViewlet):
    """View interface for OrderListingViewlet"""

    def orders():
        """Returns list of dictionary of orders

        :rtype: list
        """

    def class_collapsible():
        """Returns styling values

        :rtype: str
        """


class IBillingAndShippingRegistrationNumberViewlet(IViewlet):
    """Viewlet interface for BillingAndShippingRegistrationNumberViewlet"""

    def registration_number():
        """Returns registration number

        :rtype: str
        """


class IOrderConfirmationRegistrationNumberViewlet(IViewlet):
    """Viewlet interface for OrderConfirmationRegistrationNumberViewlet"""

    def registration_number():
        """Returns registration number

        :rtype: str
        """
