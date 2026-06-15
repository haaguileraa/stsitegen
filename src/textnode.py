from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT   = "text"
    BOLD   = "bold"
    ITALIC = "italic"
    CODE   = "code"
    LINK   = "link"
    IMAGE  = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(textNode: TextNode) -> LeafNode:
    match textNode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textNode.text)
        case TextType.BOLD:
            return LeafNode("b", textNode.text)
        case TextType.ITALIC:
            return LeafNode("i", textNode.text)
        case TextType.CODE:
            return LeafNode("code", textNode.text)
        case TextType.LINK:
            return LeafNode("a", textNode.text, {"href": textNode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textNode.url, "alt": textNode.text})
        case _:
            raise TypeError(f"TextType \"{textNode.text_type}\" not known")

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

