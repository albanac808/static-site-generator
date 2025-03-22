import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_boot_example(self):
        final_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(len(final_nodes), 10)
        self.assertEqual(final_nodes[0].text, "This is ")
        self.assertEqual(final_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[1].text, "text")
        self.assertEqual(final_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[2].text, " with an ")
        self.assertEqual(final_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[3].text, "italic")
        self.assertEqual(final_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(final_nodes[4].text, " word and a ") 
        self.assertEqual(final_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[5].text, "code block")
        self.assertEqual(final_nodes[5].text_type, TextType.CODE)
        self.assertEqual(final_nodes[6].text, " and an ")
        self.assertEqual(final_nodes[6].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[7].text, "obi wan image")
        self.assertEqual(final_nodes[7].text_type, TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(final_nodes[8].text, " and a ")
        self.assertEqual(final_nodes[8].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[9].text, "link")
        self.assertEqual(final_nodes[9].text_type, TextType.LINK, "https://boot.dev")

    def test_simple_text(self):
        nodes = text_to_textnodes("Simple text")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Simple text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_bold_text(self):
        nodes = text_to_textnodes("This is **bold** text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_italic_text(self):
        nodes = text_to_textnodes("This is _italic_ text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
    
    def test_code_text(self):
        nodes = text_to_textnodes("This is `code` text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_link(self):
        nodes = text_to_textnodes("This is a [link](https://boot.dev) text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://boot.dev")
    
    def test_image(self):
        nodes = text_to_textnodes("This is an ![image](https://example.com/img.jpg) text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.jpg")
    
    def test_multiple_elements(self):
        nodes = text_to_textnodes("**Bold** and _italic_ and `code`")
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text_type, TextType.CODE)

    def test_nested_elements(self):
        # Since we're not handling true nested elements, let's test with separate elements
        nodes = text_to_textnodes("This is **bold** and _italic_")
        self.assertTrue(any(node.text_type == TextType.BOLD for node in nodes))
        self.assertTrue(any(node.text_type == TextType.ITALIC for node in nodes))
    
    def test_boot_example(self):
        # Test with the example from the assignment
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        
        # Check specific nodes
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")

if __name__ == "__main__":
    unittest.main()