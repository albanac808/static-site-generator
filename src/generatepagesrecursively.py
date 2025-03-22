import os
from utils import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages for all Markdown files in the content directory.
    The generated pages are written to the public directory, maintaining the directory structure.
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
                
                # Full path to the output HTML file in the public directory
                output_path = os.path.join(dest_dir_path, output_file)
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Generate the HTML page
                print(f"Generating page for {markdown_path} -> {output_path}")
                generate_page(markdown_path, template_path, output_path)