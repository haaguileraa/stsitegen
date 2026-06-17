import unittest
from textnode import TextNode, TextType
from helpers import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_all_in_order(self):
        text: str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(nodes,
                             [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
])

    
    def test_only_code(self):
        text: str = "This is a text that contains only **one bold** and **another bold** TextTypes"
        node = TextNode(text, TextType.TEXT)
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(nodes,
                             [
                                 TextNode("This is a text that contains only ", TextType.TEXT),
                                 TextNode("one bold", TextType.BOLD),
                                 TextNode(" and ", TextType.TEXT),
                                 TextNode("another bold", TextType.BOLD),
                                 TextNode(" TextTypes", TextType.TEXT)
                             ])
    

    def test_no_value_left_as_text(self):
        text: str = "This is a text that contains no md TextTypes"
        node = TextNode(text, TextType.TEXT)
        nodes: list[TextNode] = text_to_textnodes(text) 
        self.assertListEqual([node], nodes)


if __name__ == "__main__":
    unittest.main()

