import unittest
from extractmarkdown import extract_markdown_images, extract_markdown_links

class TestMarkdownParser(unittest.TestCase):
    def test_extract_single_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_no_images(self):
        text = "This is text with no images, just [a link](https://example.com)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_single_link(self):
        text = "This is text with a [link](https://www.boot.dev)"
        expected = [("link", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_no_links(self):
        text = "This is text with no links, just an ![image](https://example.com/image.jpg)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_links_ignores_images(self):
        text = "This has ![an image](https://example.com/image.jpg) and [a link](https://example.com)"
        expected = [("a link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_complex_urls(self):
        text = "[Complex URL](https://example.com/path?query=value&another=123#fragment)"
        expected = [("Complex URL", "https://example.com/path?query=value&another=123#fragment")]
        self.assertEqual(extract_markdown_links(text), expected)