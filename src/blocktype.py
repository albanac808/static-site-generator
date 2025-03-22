from enum import Enum
import re
from extractmarkdown import extract_markdown_images, extract_markdown_links, is_markdown_image, is_markdown_link

BlockType = Enum('BlockType', ['paragraph', 'heading', 'code', 'quote', 'unordered_list', 'ordered_list'])

def is_valid_markdown_header(header):
    # Match 1-6 # characters followed by a space
    pattern = re.compile(r'^#{1,6}\s')
    return bool(pattern.match(header))

def is_sequential_ordered_list(lines):
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            return False
    return True

def block_to_block_type(block):
    lines = block.split('\n')
    
    # Check for heading
    if is_valid_markdown_header(block):
        return BlockType.heading
        
    # Check for code block
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.code
        
    # Check for quote
    elif all(line.startswith('>') for line in lines):
        return BlockType.quote

    # Check for unordered list
    elif all(line.startswith('- ') for line in lines):
        return BlockType.unordered_list
    
    # Check for ordered list
    elif is_sequential_ordered_list(lines):
        return BlockType.ordered_list

    # Check for image
    elif is_markdown_image(block):
        return BlockType.paragraph  # Treat images as part of a paragraph

    # Check for link
    elif is_markdown_link(block):
        return BlockType.paragraph  # Treat links as part of a paragraph

    # Default case
    else:
        print(f"Warning: Block does not match any known type: {block}")
        return BlockType.paragraph  # Ensure we return a valid type