import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


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


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_seven_hashes_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Too many"), BlockType.PARAGRAPH
        )

    def test_heading_requires_space(self):
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_single_line_code_is_paragraph(self):
        self.assertEqual(block_to_block_type("```single line```"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(
            block_to_block_type(">quoted\n>more quote"), BlockType.QUOTE
        )

    def test_quote_with_space(self):
        self.assertEqual(
            block_to_block_type("> quoted\n> more quote"), BlockType.QUOTE
        )

    def test_quote_mixed_lines_is_paragraph(self):
        self.assertEqual(
            block_to_block_type(">quoted\nnot quoted"), BlockType.PARAGRAPH
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item one\n- item two"), BlockType.UNORDERED_LIST
        )

    def test_unordered_list_requires_space(self):
        self.assertEqual(
            block_to_block_type("-item\n-item"), BlockType.PARAGRAPH
        )

    def test_unordered_list_mixed_lines_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("- item one\nitem two"), BlockType.PARAGRAPH
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH
        )

    def test_ordered_list_skipped_number_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH
        )

    def test_plain_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is just a normal paragraph"),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
