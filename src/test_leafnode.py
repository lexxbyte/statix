import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text.")
        self.assertEqual(node.to_html(), "<b>This is bold text.</b>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "A heading")
        self.assertEqual(node.to_html(), "<h1>A heading</h1>")

    def test_leaf_to_html_no_tag_returns_raw_text(self):
        node = LeafNode(None, "just some raw text")
        self.assertEqual(node.to_html(), "just some raw text")

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_children(self):
        node = LeafNode("p", "text")
        self.assertIsNone(node.children)

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            repr(node),
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})",
        )


if __name__ == "__main__":
    unittest.main()
