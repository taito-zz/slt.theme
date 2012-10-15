from Products.CMFCore.utils import getToolByName

import logging


PROFILE_ID = 'profile-slt.theme:default'


def update_viewlets(context, logger=None):
    """Update viewlets"""
    if logger is None:
        logger = logging.getLogger(__name__)
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting rolemap.')
    setup.runImportStepFromProfile(PROFILE_ID, 'viewlets', run_dependencies=False, purge_old=False)
