import unittest
from markdowntoblocks import markdown_to_blocks


class TestMarkdownToBlock(unittest.TestCase):
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

    def test_simple_blocks(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n- Item 1\n- Item 2"
        expected = [
            "# Heading",
            "This is a paragraph.",
            "- Item 1\n- Item 2"
        ]
        assert markdown_to_blocks(markdown) == expected

    def test_extra_blank_lines(self):
        markdown = "First block\n\n\n\nSecond block"
        expected = [
            "First block",
            "Second block"
        ]
        assert markdown_to_blocks(markdown) == expected

    def test_whitespace_only(self):
        markdown = "   \n\n"
        expected = []
        assert markdown_to_blocks(markdown) == expected

    def test_single_block(self):
        markdown = "This is all one block and has no blank lines."
        expected = [
            "This is all one block and has no blank lines."
        ]
        assert markdown_to_blocks(markdown) == expected


if __name__ == "__main__":
    unittest.main()