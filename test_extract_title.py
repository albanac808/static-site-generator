import unittest
from src.utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("No headers here")

    def test_multiple_headers(self):
        markdown = "# First Header\n## Second Header\n### Third Header"
        self.assertEqual(extract_title(markdown), "First Header")

if __name__ == "__main__":
    unittest.main()