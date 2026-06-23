import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
 
    def test_properties(self):
        text: str = "Test 1"
        text_type: TextType = TextType.LINK
        url: str = "https://www.python.org/"
        node = TextNode(text, text_type, url)
        self.assertEqual(node.text, text)
        self.assertEqual(node.text_type, text_type)
        self.assertEqual(node.url, url) 

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("Test URL", TextType.LINK, "https://www.python.org/")
        node2 = TextNode("Test URL", TextType.LINK, "https://www.python.org/")
        self.assertEqual(node, node2)

    def test_default_url(self):
        node = TextNode("Test None url", TextType.ITALIC)
        self.assertEqual(node.url, None)
   
    def test_non_objet_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.python.org/")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.python.org/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.python.org/"},
        )
        self.assertEqual(html_node.props_to_html(), " href=\"https://www.python.org/\"")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "ressources/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "ressources/img.png", "alt": "This is an image node"},
        )
        self.assertEqual(html_node.props_to_html(), " src=\"ressources/img.png\" alt=\"This is an image node\"")

if __name__ == "__main__":
    unittest.main()
