def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    print(f"Generated blocks: {blocks}")
    clean_blocks = [
        "\n".join(line.strip() for line in block.split("\n") if line.strip())
        for block in blocks if block.strip()
    ]
    print(f"Cleaned blocks: {clean_blocks}")
    return clean_blocks
            
    