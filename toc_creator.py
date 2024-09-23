import argparse
import re
import os

def generate_toc(markdown_content):
    toc = []
    for line in markdown_content.splitlines():
        match = get_1_to_6_headers(line)
        if match:
            level = get_level(match)
            title = get_title(match) 
            link = generate_anchor(title)
            append_content(toc, level, title, link)
    return "\n".join(toc)

def append_content(toc, level, title, link):
    toc.append(f"{'  ' * (level - 1)}- [{title}](#{link})")

def generate_anchor(title):
    return title.lower().replace(" ", "-")

def get_title(match):
    return match.group(2).strip()

def get_level(match):
    return len(match.group(1))

def get_1_to_6_headers(line):
    return re.match(r'^(#{1,6})\s+(.*)', line)

def insert_toc(file_path):
    markdown_content = read_markdown(file_path)
    
    toc = generate_toc(markdown_content)
    
    new_markdown = insert_toc_on_top(markdown_content, toc)
    
    write_new_markdown(file_path, new_markdown)
    
    print(f"ToC was generated and inserted in {file_path}")

def write_new_markdown(file_path, new_markdown):
    with open(file_path, 'w') as f:
        f.write(new_markdown)

def read_markdown(file_path):
    with open(file_path, 'r') as f:
        markdown_content = f.read()
    return markdown_content

def insert_toc_on_top(markdown_content, toc):
    return f"## Table of Contents\n\n{toc}\n\n{markdown_content}"

def process_file(file_path):
    if os.path.isfile(file_path):
        insert_toc(file_path)
    elif os.path.isdir(file_path):
        for filename in os.listdir(file_path):
            if filename.endswith('.md'):
                full_path = os.path.join(file_path, filename)
                insert_toc(full_path)
    else:
        print(f"El path especificado no es un archivo ni un directorio: {file_path}")

def main(file_path):
    process_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a dynamic Table of Contents for a Markdown file or folder")
    parser.add_argument("file_path", type=str, help="Path of the Markdown file or folder")
    
    args = parser.parse_args()
    main(str(args.file_path))
