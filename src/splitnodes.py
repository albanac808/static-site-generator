import re
from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            # No images found, keep node as is
            new_nodes.append(old_node)
            continue
        
        # Start with the current text
        remaining_text = text
        
        # Process each image
        for image_alt, image_url in images:
            # Split the text at the image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            # Add node for text before image (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add node for the image
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update remaining text to what comes after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
          
        # Add any remaining text as a node (if not empty)
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            # No links found, keep node as is
            new_nodes.append(old_node)
            continue
        
        # Start with the current text
        remaining_text = text
        
        # Process each link
        for link_alt, link_url in links:
            # Split the text at the link markdown
            link_markdown = f"[{link_alt}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            
            # Add node for text before image (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add node for the image
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            
            # Update remaining text to what comes after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text as a node (if not empty)
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes
