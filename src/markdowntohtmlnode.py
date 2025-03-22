from markdowntoblocks import markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from splitnodes import split_nodes_image, split_nodes_link
from splitdelimiter import split_nodes_delimiter


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text or "")
    elif text_node.text_type == TextType.BOLD:
        return ParentNode("b", [LeafNode(None, text_node.text or "")])
    elif text_node.text_type == TextType.ITALIC:
        return ParentNode("i", [LeafNode(None, text_node.text or "")])
    elif text_node.text_type == TextType.CODE:
        return ParentNode("code", [LeafNode(None, text_node.text or "")])
    elif text_node.text_type == TextType.LINK:
        return ParentNode("a", [LeafNode(None, text_node.text or "")], {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")


def extract_markdown_text(text):
    if not text:
        return [TextNode("", TextType.TEXT)]
    
    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process delimiters for bold, italic, code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Process links and images
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Ensure we return at least one node
    if not nodes:
        print(f"Warning: No nodes extracted from text: {text}")
        return [TextNode("", TextType.TEXT)]
    
    return nodes


def text_to_children(text):
    # First, parse the text into TextNode objects (bold, italic, links, etc.)
    text_nodes = extract_markdown_text(text)
    
    # Convert TextNode objects to appropriate HTML nodes
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    
    return children


def markdown_to_html_node(markdown):
    if not markdown.strip():
        print("Warning: Markdown content is empty or invalid.")
        return ParentNode("div", [LeafNode(None, "")])  # Return an empty div
    
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Processing block: {block[:30]}... (type: {block_type})")

        # Handle each block type
        if block_type == BlockType.heading:
            level = block.count("#")
            content = block[level:].strip()
            if not content:
                print(f"Warning: Empty heading block detected: {block}")
                continue
            children = text_to_children(content)
            all_nodes.append(ParentNode(f"h{level}", children))

        elif block_type == BlockType.paragraph:
            children = text_to_children(block)
            if not children:
                print(f"Warning: Empty paragraph block detected: {block}")
                continue
            all_nodes.append(ParentNode("p", children))

        elif block_type == BlockType.code:
            content = "\n".join(block.split("\n")[1:-1])  # Remove backticks
            if not content.strip():
                print(f"Warning: Empty code block detected: {block}")
                continue
            code_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, content)])])
            all_nodes.append(code_node)

        elif block_type == BlockType.quote:
            content = "\n".join([line[1:].strip() for line in block.split("\n") if line.strip()])
            if not content.strip():
                print(f"Warning: Empty quote block detected: {block}")
                continue
            
            # Create a LeafNode with the raw content
            all_nodes.append(ParentNode("blockquote", [LeafNode(None, content)]))

        elif block_type == BlockType.unordered_list:
            items = [line[2:].strip() for line in block.split("\n") if line.strip()]
            list_items = [ParentNode("li", text_to_children(item)) for item in items]
            all_nodes.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ordered_list:
            items = [line.split(". ", 1)[1].strip() for line in block.split("\n") if ". " in line]
            list_items = [ParentNode("li", text_to_children(item)) for item in items]
            all_nodes.append(ParentNode("ol", list_items))

    if not all_nodes:
        print("Warning: No valid nodes found in the Markdown content.")
        return ParentNode("div", [LeafNode(None, "")])  # Return an empty div
    
    return ParentNode("div", all_nodes)