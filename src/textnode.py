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
