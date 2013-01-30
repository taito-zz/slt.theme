from Products.CMFCore.utils import getToolByName
from abita.utils.utils import reimport_profile

import logging


PROFILE_ID = 'profile-slt.theme:default'


def reimport_registry(context, logger=None):
    """Reimport registry"""
    if logger is None:
        logger = logging.getLogger(__name__)
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting registry.')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)


def reimport_viewlets(context, logger=None):
    """Reimport viewlets"""
    if logger is None:
        logger = logging.getLogger(__name__)
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting viewlets.')
    setup.runImportStepFromProfile(PROFILE_ID, 'viewlets', run_dependencies=False, purge_old=False)


def reimport_cssregistry(context):
    reimport_profile(context, PROFILE_ID, 'cssregistry')


def reimport_rolemap(context):
    reimport_profile(context, PROFILE_ID, 'rolemap')


def clean_viewlets(manager, skinname):
    from zope.component import getUtility
    from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
    storage = getUtility(IViewletSettingsStorage)
    message = 'Cleaning viewlets from {} for {}'.format(manager, skinname)
    logger = logging.getLogger(__name__)
    logger.info(message)
    storage.setHidden(manager, skinname, [])
    storage.setOrder(manager, skinname, [])


def clean_viewlets_from_collective_cart_shopping_billing_shipping_manager(context):
    """Clean viewlets from collective.cart.shopping.billing.shipping.manager"""
    clean_viewlets(u'collective.cart.shopping.billing.shipping.manager', u'Plone Default')
    clean_viewlets(u'collective.cart.shopping.billing.shipping.manager', u'Sunburst Theme')
    clean_viewlets(u'collective.cart.shopping.billing.shipping.manager', u'*')
