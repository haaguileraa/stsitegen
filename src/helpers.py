import re
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images_re: str = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(images_re, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links_re: str = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(links_re, text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if old_nodes is None or len(old_nodes) == 0:
        raise ValueError("cannot process an empty node")
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_parts: list[str] = old_node.text.split(delimiter)
        n_parts: int = len(text_parts)
        if  n_parts == 1 or n_parts % 2 == 0:
            raise SyntaxError(f"invalid markdown syntax: text \"{old_node.text}\" does not contain a matching number of delimiters '{delimiter}'")
        nodes_in_old_node: list[TextNode] = []
        for i in range(n_parts):
            current_text_type: TextType | None = None
            if i % 2 == 0:
                current_text_type = TextType.TEXT
            else:
                current_text_type = text_type
            nodes_in_old_node.append(TextNode(text_parts[i], current_text_type)) 
        new_nodes.extend(nodes_in_old_node)
    return new_nodes


def get_text_type_from_delimiter(delimiter: str) -> TextType:
    match delimiter:
        case "**":
            return TextType.BOLD
        case "_":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case _:
            raise ValueError(f"cannot convert delimiter '{delimiter}' in TextType")

