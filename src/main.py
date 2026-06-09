from textnode import TextType, TextNode

def main() -> None:
    text: str = "test link text"
    text_type: TextType = TextType.LINK_TEXT_TYPE
    url: str = "https://github.com/"
    text_node: TextNode = TextNode(text, text_type, url)
    print(text_node)

if __name__ == "__main__":
        main()
