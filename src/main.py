import os
import shutil
import sys
from utils import copy_directory_recursive, generate_pages_recursive

def main():
    # Define paths
    source_dir = "static"
    destination_dir = "docs"  # Change to "docs" for GitHub Pages
    content_dir = "content"
    template_path = "template.html"

    # Get the base path from the command-line argument or default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Step 1: Clear the docs directory
    if os.path.exists(destination_dir):
        print(f"Clearing the docs directory: {destination_dir}")
        shutil.rmtree(destination_dir)

    # Step 2: Copy static files to the docs directory
    print(f"Copying static files from {source_dir} to {destination_dir}")
    copy_directory_recursive(source_dir, destination_dir)

    # Step 3: Generate HTML pages recursively with the base path
    print(f"Generating HTML pages from {content_dir} with base path: {base_path}")
    generate_pages_recursive(content_dir, template_path, destination_dir, base_path)

if __name__ == "__main__":
    main()