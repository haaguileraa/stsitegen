import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images_re: str = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(images_re, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links_re: str = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(links_re, text)
