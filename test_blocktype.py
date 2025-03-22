import unittest
from blocktype import block_to_block_type, BlockType

class TestBlockType(unittest.TestCase):
    
    # Paragraph tests
    def test_simple_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_multiline_paragraph(self):
        block = "This is a paragraph\nwith multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    # Heading tests
    def test_heading_level_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.heading)
    
    def test_heading_level_6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.heading)
    
    def test_invalid_heading_no_space(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_invalid_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    # Code block tests
    def test_empty_code_block(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.code)
    
    def test_code_block_with_content(self):
        block = "```\ndef hello():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.code)
    
    def test_invalid_code_block_missing_end(self):
        block = "```\ndef hello():\n    print('Hello, world!')"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_invalid_code_block_missing_start(self):
        block = "def hello():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    # Quote tests
    def test_single_line_quote(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.quote)
    
    def test_multiline_quote(self):
        block = ">Line 1\n>Line 2\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.quote)
    
    def test_invalid_quote_missing_prefix(self):
        block = ">Line 1\nLine 2\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    # Unordered list tests
    def test_single_item_unordered_list(self):
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)
    
    def test_multi_item_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)
    
    def test_invalid_unordered_list_missing_space(self):
        block = "-Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_invalid_unordered_list_missing_prefix(self):
        block = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    # Ordered list tests
    def test_single_item_ordered_list(self):
        block = "1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)
    
    def test_multi_item_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)
    
    def test_invalid_ordered_list_wrong_sequence(self):
        block = "1. Item 1\n3. Item 3\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_invalid_ordered_list_not_starting_at_1(self):
        block = "2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_invalid_ordered_list_missing_space(self):
        block = "1.Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    # Edge cases
    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_whitespace_only_block(self):
        block = "   \n  \n    "
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_mixed_content_block(self):
        block = "First line\n- Not a list\n1. Not ordered"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_almost_heading(self):
        block = "##Almost a heading"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_almost_code_block(self):
        block = "``Almost a code block``"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_partial_quote(self):
        block = ">First line\nSecond line without quote"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_code_block_with_backticks_inside(self):
        block = "```\n`inline code`\n```"
        self.assertEqual(block_to_block_type(block), BlockType.code)
    
    def test_nested_structure(self):
        block = "- List item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)

if __name__ == '__main__':
    unittest.main()