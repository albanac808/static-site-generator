import os
import re
import shutil
from pathlib import Path
from markdowntohtmlnode import markdown_to_html_node
from bs4 import BeautifulSoup
import markdown


def copy_directory_recursive(source, destination):
    """
    Recursively copies all contents from the source directory to the destination directory.
    Clears the destination directory before copying.
    Logs each file and directory being copied.
    """
    # Step 1: Ensure the destination directory is clean
    if os.path.exists(destination):
        print(f"Deleting contents of destination directory: {destination}")
        shutil.rmtree(destination)  # Remove all contents of the destination directory
    os.mkdir(destination)  # Recreate the destination directory

    # Step 2: Recursively copy contents from source to destination
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)

        if os.path.isfile(source_item):
            # Copy file and log the action
            shutil.copy(source_item, destination_item)
            print(f"Copied file: {source_item} -> {destination_item}")
        elif os.path.isdir(source_item):
            # Recursively copy subdirectory
            print(f"Entering directory: {source_item}")
            copy_directory_recursive(source_item, destination_item)



def extract_title(markdown):
    """
    Extract the h1 title from markdown content.
    
    Args:
        markdown (str): The markdown content to extract from
        
    Returns:
        str: The extracted title text
        
    Raises:
        Exception: If no h1 header is found
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            # Strip the '# ' prefix and any leading/trailing whitespace
            return line[2:].strip()
    
    # If no h1 header is found, raise an exception
    raise Exception("No h1 header found in the markdown content")




def adjust_image_paths(html_content):
    """
    Adjusts all image paths in the HTML to be absolute paths starting with /images/.

    Args:
        html_content (str): The HTML content.

    Returns:
        str: HTML content with updated image paths.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and not src.startswith("/images/"):
            # Ensure images point to /images/ directory
            filename = os.path.basename(src)  # Extract the image filename
            img["src"] = f"/images/{filename}"  # Convert to absolute path

    return str(soup)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    """
    Recursively generates HTML pages for all Markdown files in the content directory.
    The generated pages are written to the docs directory, maintaining the directory structure.
    """
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):  # Process only Markdown files
                # Full path to the Markdown file
                markdown_path = os.path.join(root, file)
                
                # Determine the relative path from the content directory
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                
                # Replace .md with .html for the output file
                output_file = relative_path.replace(".md", ".html")
                
                # Full path to the output HTML file in the docs directory
                output_path = os.path.join(dest_dir_path, output_file)
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Generate the HTML page with the base path
                print(f"Generating page for {markdown_path} -> {output_path}")
                generate_page(markdown_path, template_path, output_path, base_path)


def generate_page(content_path, template_path, output_path, base_path):
    """
    Generates an HTML page from a Markdown file using a template.
    Replaces href="/ and src="/ with href="{BASEPATH}" and src="{BASEPATH}".
    """
    # Read the Markdown content
    with open(content_path, "r") as content_file:
        markdown_content = content_file.read()

    # Read the template
    with open(template_path, "r") as template_file:
        template = template_file.read()

    # Convert Markdown to HTML
    from markdowntohtmlnode import markdown_to_html_node
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Replace placeholders in the template
    html_output = template.replace("{{ Content }}", html_content)
    html_output = html_output.replace("{{ Title }}", os.path.basename(content_path).replace(".md", ""))
    
    # Replace href="/ and src="/ with the base path
    html_output = html_output.replace('href="/', f'href="{base_path}')
    html_output = html_output.replace('src="/', f'src="{base_path}')

    # Write the output HTML file
    with open(output_path, "w") as output_file:
        output_file.write(html_output)