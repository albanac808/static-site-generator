import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):

# TESTING PARENTNODE CLASS

    def test_tag_eq(self):
        node1 = HTMLNode("p", "This is my paragraph")
        node2 = HTMLNode("p", "This is my paragraph")
        self.assertEqual(node1.tag, node2.tag)

    def test_value_eq(self):
        node3 = HTMLNode("p", "This is my paragraph", None, None)
        node4 = HTMLNode("p", "This is my paragraph")
        self.assertEqual(node3.value, node4.value)

    def test_different_types(self):
        node3 = HTMLNode("a", None, None, {"href": "http://www.google.com"})
        node4 = HTMLNode("p", "This is my paragraph")
        # Compare `tag` instead of the whole objects
        self.assertNotEqual(node3.tag, node4.tag)

    def test_props_to_html(self):
        node = HTMLNode("a", "Link", props={"href": "http://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="http://example.com" target="_blank"')
        empty_node = HTMLNode("a", "Empty Props", props={})
        self.assertEqual(empty_node.props_to_html(), "")

    def test_to_html_not_implemented(self):
        node = HTMLNode("div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_nested_children(self):
        child = HTMLNode("span", "child text")
        parent = HTMLNode("div", None, children=[child])
        self.assertIsInstance(parent.children[0], HTMLNode)
        self.assertEqual(parent.children[0].tag, "span")


# TESTING LEAFNODE CLASS

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com", "class": "link"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" class="link">Click me</a>')
        # Or you might need to check if it contains both properties in any order

    def test_leaf_to_html_empty_value_raises(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_none_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_self_closing_tag(self):
        # This tests if your implementation handles special self-closing tags correctly
        # You might need to add special handling for these
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image">')


# TESTING PARENTNODE CLASS

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nochildren(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()


# TESTING CONVERTERS.PY

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_node_conversion(self):
        # Test converting a link text node
        link_node = TextNode("Click here", TextType.LINK)
        link_node.url = "https://example.com"
        html_node = text_node_to_html_node(link_node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image_node_conversion(self):
        # Test converting an image text node
        image_node = TextNode("Alt text for image", TextType.IMAGE) 
        image_node.url = "https://example.com/image.png"
        html_node = text_node_to_html_node(image_node)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Empty string value for img
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text for image")


 # PARAGRAPHNODE SPECIAL TESTING       

    class ParagraphNode(HTMLNode):
        def to_html(self):
            return f"<p>{self.value}</p>"

        def test_paragraph_node_to_html(self):
            node = ParagraphNode(value="I am a paragraph.")
            self.assertEqual(node.to_html(), "<p>I am a paragraph.</p>")

if __name__ == "__main__":
    unittest.main()