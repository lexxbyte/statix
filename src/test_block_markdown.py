import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """

# Heading


Paragraph here.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Paragraph here."])

    def test_markdown_to_blocks_single_block(self):
        blocks = markdown_to_blocks("Just one block")
        self.assertEqual(blocks, ["Just one block"])

    def test_markdown_to_blocks_strips_whitespace(self):
        md = "   # Heading with spaces around it   \n\n   Paragraph with spaces.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# Heading with spaces around it", "Paragraph with spaces."],
        )

    def test_markdown_to_blocks_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks_three_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(
            blocks[1],
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
        )
        self.assertEqual(
            blocks[2],
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        )


if __name__ == "__main__":
    unittest.main()
