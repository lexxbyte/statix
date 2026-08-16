import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_with_surrounding_content(self):
        md = """# My Title

Some paragraph text here.

## A subheading
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Spaced Title   "), "Spaced Title")

    def test_extract_title_not_first_block(self):
        md = """Some paragraph first.

# The Actual Title

More content.
"""
        self.assertEqual(extract_title(md), "The Actual Title")

    def test_extract_title_ignores_h2(self):
        md = """## Not an h1

# Real Title
"""
        self.assertEqual(extract_title(md), "Real Title")

    def test_extract_title_no_h1_raises(self):
        md = """No title here

## Only an h2
"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_empty_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
