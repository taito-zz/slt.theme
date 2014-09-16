from slt.theme.userdataschema import BirthDateValidationError

import unittest


class ValidateBirthDateTestCase(unittest.TestCase):
    """TestCase for validate_birth_date"""

    def test(self):
        from slt.theme.userdataschema import validate_birth_date
        with self.assertRaises(BirthDateValidationError):
            validate_birth_date('aaa')
