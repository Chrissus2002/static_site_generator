from block_markdown import markdown_to_blocks, block_to_block_type
import unittest

class TestMarkdownBlock(unittest.TestCase):
    def test_two_block(self):
        markdown = "This is just a paragraph\n\n \n\n ##This is a heading 2"
        self.assertEqual(["This is just a paragraph","##This is a heading 2"], markdown_to_blocks(markdown))
    def test_list_block(self):
        markdown = "   *Item 1\n*Item 2\n*Item 3   "
        self.assertEqual(["*Item 1\n*Item 2\n*Item 3"],markdown_to_blocks(markdown))
    def test_block_to_heading(self):
        text = "## This is a heading 2"
        self.assertEqual('heading', block_to_block_type(text))
    def test_block_to_code(self):
        text = "```this is a block of code```"
        self.assertEqual('code', block_to_block_type(text))
    def test_block_to_quote(self):
        text = "> This are\n> some quotes\n> in the text"
        self.assertEqual('quote', block_to_block_type(text))
    def test_block_to_unordered_list(self):
        text = "- item 1\n- item 2\n- item 3"
        self.assertEqual('unordered list', block_to_block_type(text))
    def test_block_to_ordered_list(self):
        text = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual('ordered list', block_to_block_type(text))
    def test_block_to_paragraph(self):
        text = "This is just some normal text *with some bold letters*"
        self.assertEqual('paragraph', block_to_block_type(text))

if __name__ == "__main__":
    unittest.main()