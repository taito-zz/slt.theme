from five import grok
from slt.theme.interfaces import ICollapsedOnLoad
from zope.interface import implements


class CollapsedOnLoad(grok.GlobalUtility):
    implements(ICollapsedOnLoad)

    def __call__(self, collapsed=True):
        if collapsed:
            return 'collapsible collapsedOnLoad'
        return 'collapsible'
