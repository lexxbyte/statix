import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_mixed_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [LeafNode("a", "item one", {"href": "https://example.com"})],
                        ),
                        ParentNode("li", [LeafNode("b", "item two")]),
                    ],
                ),
                LeafNode("p", "footer text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><ul><li><a href="https://example.com">item one</a></li>'
            "<li><b>item two</b></li></ul><p>footer text</p></div>",
        )

    def test_to_html_no_children_renders_empty(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )

    def test_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_value_is_always_none(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.value)

    def test_repr(self):
        child = LeafNode("span", "child")
        node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            repr(node),
            "ParentNode(div, [LeafNode(span, child, None)], {'class': 'container'})",
        )


if __name__ == "__main__":
    unittest.main()
