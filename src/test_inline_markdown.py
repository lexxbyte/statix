import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("Some _italic text_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_no_delimiter_returns_original(self):
        node = TextNode("plain text with nothing special", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_multiple_delimited_sections(self):
        node = TextNode("a **one** b **two** c", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
                TextNode(" b ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" c", TextType.TEXT),
            ],
        )

    def test_delimiter_at_edges(self):
        node = TextNode("**whole thing**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("whole thing", TextType.BOLD)])

    def test_non_text_nodes_pass_through(self):
        bold = TextNode("bold", TextType.BOLD)
        text = TextNode("with `code` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold, text], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" inside", TextType.TEXT),
            ],
        )

    def test_empty_sections_skipped(self):
        node = TextNode("start `end`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("end", TextType.CODE),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_multiple_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            extract_markdown_links(text),
        )

    def test_extract_multiple_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_links_do_not_match_images(self):
        text = "An image ![alt](https://example.com/img.png) is not a link"
        self.assertListEqual([], extract_markdown_links(text))

    def test_images_do_not_match_links(self):
        text = "A link [anchor](https://example.com) is not an image"
        self.assertListEqual([], extract_markdown_images(text))

    def test_no_matches_returns_empty(self):
        self.assertListEqual([], extract_markdown_images("plain text"))
        self.assertListEqual([], extract_markdown_links("plain text"))


if __name__ == "__main__":
    unittest.main()
