import logging


logger = logging.getLogger(__name__)


def set_doctype():
    """Set doctype to <!DOCTYPE html>."""
    from plone.app.theming.interfaces import IThemeSettings
    from plone.registry.interfaces import IRegistry
    from zope.component import getUtility
    view = getUtility(IRegistry).forInterface(IThemeSettings)
    view.doctype = '<!DOCTYPE html>'


def setupVarious(context):

    if context.readDataFile('slt.theme_various.txt') is None:
        return

    set_doctype()
