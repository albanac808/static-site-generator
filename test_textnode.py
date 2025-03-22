import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_no_url(self):
        url_none = TextNode("This is a text node", TextType.BOLD, None)
        code_type = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(url_none, code_type)
    
    def test_different_urls(self):
        node1 = TextNode("Same text", TextType.LINK, "http://example.com")
        node2 = TextNode("Same text", TextType.LINK, "http://different.com")
        self.assertNotEqual(node1, node2)

    def test_different_types(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()