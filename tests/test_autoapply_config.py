import unittest

from autoapply.config import reject_placeholders


class ConfigurationValidationTests(unittest.TestCase):
    def test_non_string_yaml_keys_are_rejected_with_country_hint(self):
        with self.assertRaisesRegex(ValueError, 'quote country codes such as "NO"'):
            reject_placeholders({"work_authorization": {False: {}}})


if __name__ == "__main__":
    unittest.main()
