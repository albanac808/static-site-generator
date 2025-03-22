import unittest
from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and this is also **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " and this is also ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
    
    def test_delimiter_at_start(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " at the start")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        
    def test_delimiter_at_end(self):
        node = TextNode("At the end is **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "At the end is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        
    def test_missing_closing_delimiter(self):
        node = TextNode("This has **no closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
            
    def test_non_text_node(self):
        # Non-text nodes should pass through unchanged
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        
    def test_multiple_nodes(self):
        node1 = TextNode("This is **bold**", TextType.TEXT)
        node2 = TextNode("This is _italic_", TextType.TEXT)
        node3 = TextNode("Regular text", TextType.TEXT)
        
        # First split for bold
        intermediate_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        # Then split for italic
        final_nodes = split_nodes_delimiter(intermediate_nodes, "_", TextType.ITALIC)
        
        self.assertEqual(len(final_nodes), 5)
        self.assertEqual(final_nodes[0].text, "This is ")
        self.assertEqual(final_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[1].text, "bold")
        self.assertEqual(final_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[2].text, "This is ")
        self.assertEqual(final_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[3].text, "italic")
        self.assertEqual(final_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(final_nodes[4].text, "Regular text")
        self.assertEqual(final_nodes[4].text_type, TextType.TEXT)
        
    def test_no_delimiters(self):
        node = TextNode("This has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This has no delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()