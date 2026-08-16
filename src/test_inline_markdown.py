import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image_no_other_text(self):
        node = TextNode("![only image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only image", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_image_with_trailing_text(self):
        node = TextNode("look at this ![image](https://example.com/i.png) wow", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("look at this ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/i.png"),
                TextNode(" wow", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_images_returns_original(self):
        node = TextNode("no images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_non_text_nodes_pass_through(self):
        bold = TextNode("bold", TextType.BOLD)
        text = TextNode("with ![image](https://example.com/i.png) inside", TextType.TEXT)
        new_nodes = split_nodes_image([bold, text])
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/i.png"),
                TextNode(" inside", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_single_link_no_other_text(self):
        node = TextNode("[only link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("only link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_link_with_trailing_text(self):
        node = TextNode("visit [boot dev](https://www.boot.dev) now", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("visit ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_links_returns_original(self):
        node = TextNode("no links here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_nodes_pass_through(self):
        code = TextNode("code", TextType.CODE)
        text = TextNode("with [link](https://example.com) inside", TextType.TEXT)
        new_nodes = split_nodes_link([code, text])
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode("with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" inside", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_images_are_not_split_by_link_splitter(self):
        node = TextNode("an ![image](https://example.com/i.png) stays", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain_text(self):
        nodes = text_to_textnodes("just plain text")
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], nodes)

    def test_text_to_textnodes_only_bold(self):
        nodes = text_to_textnodes("**bold only**")
        self.assertListEqual([TextNode("bold only", TextType.BOLD)], nodes)

    def test_text_to_textnodes_multiple_of_same_type(self):
        nodes = text_to_textnodes("one **bold** two **strong** three")
        self.assertListEqual(
            [
                TextNode("one ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" two ", TextType.TEXT),
                TextNode("strong", TextType.BOLD),
                TextNode(" three", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic_and_code(self):
        nodes = text_to_textnodes("_italic_ and `code`")
        self.assertListEqual(
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        self.assertListEqual([], text_to_textnodes(""))


if __name__ == "__main__":
    unittest.main()
