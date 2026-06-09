import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
