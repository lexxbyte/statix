import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3\n\n#### Heading 4\n\n##### Heading 5\n\n###### Heading 6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3>"
            "<h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_quote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote>"
            "<p>this is paragraph text</p></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
- and _more_ items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li>"
            "<li>and <i>more</i> items</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is a list
2. with items
3. and **more** items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li>"
            "<li>and <b>more</b> items</li></ol></div>",
        )

    def test_paragraph_with_links_and_images(self):
        md = """
Here is a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Here is a <a href="https://boot.dev">link</a> and an '
            '<img src="https://i.imgur.com/zjjcJKZ.png" alt="image"></img></p></div>',
        )

    def test_single_paragraph_plain(self):
        md = "Just a plain paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Just a plain paragraph.</p></div>")

    def test_empty_document(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
