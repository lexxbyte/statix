import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("first text", TextType.TEXT)
        node2 = TextNode("second text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("same text", TextType.BOLD)
        node2 = TextNode("same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("anchor text", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_not_eq_url_none_vs_url_set(self):
        node = TextNode("anchor text", TextType.LINK)
        node2 = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(anchor text, link, https://www.boot.dev)")


if __name__ == "__main__":
    unittest.main()
