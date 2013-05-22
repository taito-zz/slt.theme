# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Testing import ZopeTestCase as ztc
from collective.cart.core.interfaces import IShoppingSiteRoot
from hexagonit.testing.browser import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing import layered
from slt.theme.tests.base import FUNCTIONAL_TESTING
from zope.interface import alsoProvides
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    portal = layer['portal']
    app = layer['app']
    browser = Browser(app)
    self.globs.update({
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
        'browser': browser,
        'portal': portal,
    })
    ztc.utils.setupCoreSessions(app)
    browser.setBaseUrl(portal.absolute_url())
    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()
    setRoles(portal, TEST_USER_ID, ['Manager'])

    alsoProvides(portal, IShoppingSiteRoot)

    # Add two members
    regtool = getToolByName(portal, 'portal_registration')

    member1 = 'member1'
    regtool.addMember(member1, member1)
    setRoles(portal, member1, ['Member'])

    member2 = 'member2'
    regtool.addMember(member2, member2)
    setRoles(portal, member2, ['Member'])

    member3 = 'member3'
    regtool.addMember(member3, member3)
    setRoles(portal, member3, ['Member'])

    member4 = 'member4'
    regtool.addMember(member4, member4)
    setRoles(portal, member4, ['Member', 'Site Administrator'])

    membership = getToolByName(portal, 'portal_membership')
    member2 = membership.getMemberById('member2')
    member2.setMemberProperties({'allow_direct_marketing': True, 'email': 'member2@member.ml', 'fullname': 'Full Name 2'})
    member3 = membership.getMemberById('member3')
    member3.setMemberProperties({'allow_direct_marketing': True, 'email': 'member3@member.ml', 'fullname': 'Full Name 3'})

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([
        DocFileSuite('functional/members.txt')])
