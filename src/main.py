import os
import shutil
from utils import copy_directory_recursive, generate_page, generate_pages_recursive

def main():
    # Define paths
    content_dir = "content"
    template_path = "template.html"
    public_dir = "public"
    
    # Clear the public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    # Create a fresh public directory
    os.makedirs(public_dir)
    
    # Copy static assets
    copy_directory_recursive("static", public_dir)
    
    # Generate all pages recursively
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()