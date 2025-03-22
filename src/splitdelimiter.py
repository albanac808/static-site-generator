from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        # If not a text node, add it unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        # Check if this text node contains the delimiter
        text = node.text
        delimiter_index = text.find(delimiter)
        
        # If no delimiter found, add node unchanged
        if delimiter_index == -1:
            new_nodes.append(node)
            continue
            
        # Handle text before the opening delimiter
        if delimiter_index > 0:
            new_nodes.append(TextNode(text[:delimiter_index], TextType.TEXT))
            
        # Find the closing delimiter
        text_after_delimiter = text[delimiter_index + len(delimiter):]
        closing_index = text_after_delimiter.find(delimiter)
        
        if closing_index == -1:
            raise Exception(f"No closing delimiter '{delimiter}' found")
            
        # Add the delimited text with the specified type
        delimited_text = text_after_delimiter[:closing_index]
        new_nodes.append(TextNode(delimited_text, text_type))
        
        # Process any remaining text after the closing delimiter
        remaining_text = text_after_delimiter[closing_index + len(delimiter):]
        if remaining_text:
            # Create a text node from the remaining text
            remaining_node = TextNode(remaining_text, TextType.TEXT)
            # Recursively process this node for more delimiter pairs
            result_nodes = split_nodes_delimiter([remaining_node], delimiter, text_type)
            # Add all resulting nodes to our list
            new_nodes.extend(result_nodes)
    return new_nodes
