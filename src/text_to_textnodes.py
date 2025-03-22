from textnode import TextNode, TextType
from splitnodes import split_nodes_image, split_nodes_link
from splitdelimiter import split_nodes_delimiter
from extractmarkdown import extract_markdown_images, extract_markdown_links
from converters import text_node_to_html_node

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply each splitting function in sequence
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC)  # Process italic first
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)  # Then bold
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    return nodes