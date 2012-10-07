import mock
import unittest


class TestCase(unittest.TestCase):
    """Test function: setupVarious."""

    def test(self):
        from slt.theme.setuphandlers import setupVarious
        context = mock.Mock()
        context.readDataFile.return_value = None
        setupVarious(context)
        context.readDataFile.assert_call_with('slt.theme_various.txt')
