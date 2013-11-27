import logging


PROFILE_ID = 'profile-slt.theme:default'


def reimport_actions(setup):
    """Reimport actions"""
    setup.runImportStepFromProfile(PROFILE_ID, 'actions', run_dependencies=False, purge_old=False)


def reimport_cssregistry(setup):
    """Reimport cssregistry"""
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry', run_dependencies=False, purge_old=False)


def reimport_jsregistry(setup):
    """Reimport jsregistry"""
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry', run_dependencies=False, purge_old=False)


def reimport_memberdata_properties(setup):
    """Reimport memberdata-properties"""
    setup.runImportStepFromProfile(PROFILE_ID, 'memberdata-properties', run_dependencies=False, purge_old=False)


def reimport_registry(setup):
    """Reimport registry"""
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)


def reimport_rolemap(setup):
    """Reimport rolemap"""
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap', run_dependencies=False, purge_old=False)


def reimport_viewlets(setup):
    """Reimport viewlets"""
    setup.runImportStepFromProfile(PROFILE_ID, 'viewlets', run_dependencies=False, purge_old=False)


def clean_viewlets(manager, skinname):
    from zope.component import getUtility
    from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
    storage = getUtility(IViewletSettingsStorage)
    message = 'Cleaning viewlets from {} for {}'.format(manager, skinname)
    logger = logging.getLogger(__name__)
    logger.info(message)
    storage.setHidden(manager, skinname, [])
    storage.setOrder(manager, skinname, [])
