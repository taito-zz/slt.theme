from slt.theme.tests.base import ROBOT_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot/test_hello.robot'),
                layer=ROBOT_TESTING),
    ])
    return suite