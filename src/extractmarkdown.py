import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def is_markdown_image(block):
    """
    Checks if the block is a Markdown image.
    """
    pattern = re.compile(r"^!\[.*\]\(.*\)$")  # Matches ![alt text](url)
    return bool(pattern.match(block))

def is_markdown_link(block):
    """
    Checks if the block is a Markdown link.
    """
    pattern = re.compile(r"^\[.*\]\(.*\)$")  # Matches [text](url)
    return bool(pattern.match(block))