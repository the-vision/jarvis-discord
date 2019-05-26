import os
import unittest
import pep8


class TestCodeFormat(unittest.TestCase):
    def test_pep8_conformance(self):
        """Test that we conform to PEP8. checks all project files"""
        errors = 0
        style = pep8.StyleGuide(quiet=False)
        style.options.max_line_length = 120
        for root, dirs, files in os.walk("."):
            python_files = [os.path.join(root, f) for f in files if f.endswith(".py")]
            errors = style.check_files(python_files).total_errors

        self.assertEqual(errors, 0, "PEP8 style errors: %d" % errors)


if __name__ == "__main__":
    unittest.main()
