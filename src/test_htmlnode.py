import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_def_constructor(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_constructor(self):
        tag: str = "p"
        value: str = "value test"
        props: dict[str, str] = {
                "href": "https://www.google.com", 
                "target": "_blank",
                }
        node = HTMLNode(tag=tag, value=value, props=props)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, props)

    def test_props_to_html(self):
        props: dict[str, str] = {
                "href": "https://www.google.com", 
                "target": "_blank",
                }
        result: str = " href=\"https://www.google.com\" target=\"_blank\""
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), result)
    
