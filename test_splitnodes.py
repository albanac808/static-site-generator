import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_image_simple(self):
        # Test with a single image
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_multiple(self):
        # Test with multiple images
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        # Test with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_non_text_nodes(self):
        # Test with non-text nodes (should remain unchanged)
        node = TextNode("image alt", TextType.IMAGE, "https://example.com/image.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_simple(self):
        # Test with a single link
        node = TextNode(
            "This is text with a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple(self):
        # Test with multiple links
        node = TextNode(
            "This is text with [one link](https://www.boot.dev) and [another link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("one link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        # Test with no links
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_non_text_nodes(self):
        # Test with non-text nodes (should remain unchanged)
        node = TextNode("link text", TextType.LINK, "https://example.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_multiple_input_nodes(self):
        # Test with multiple input nodes
        nodes = [
            TextNode("Text with a [link](https://example.com)", TextType.TEXT),
            TextNode("Plain text", TextType.TEXT),
            TextNode("Text with an ![image](https://example.com/img.png)", TextType.TEXT)
        ]
        # Test links
        link_nodes = split_nodes_link(nodes)
        self.assertEqual(4, len(link_nodes))
        # Test images
        image_nodes = split_nodes_image(nodes)
        self.assertEqual(4, len(image_nodes))