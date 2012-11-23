from zope.interface import Interface


class IFeedToShopTop(Interface):
    """A marker interface for feed to shop top page."""


class ICollapsedOnLoad(Interface):
    """Global utility interface for class collapsedOnLoad."""

    def __call__():  # pragma: no cover
        """Returns class name for style sheet."""
