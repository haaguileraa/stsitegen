import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_none_value_error(self):
        node = LeafNode("p", "", None)
        self.assertRaises(ValueError, node.to_html) 
        node = LeafNode("p", None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_empty_tag(self):
        value: str = "Hello, world!"
        node = LeafNode("", value, None)
        self.assertEqual(node.to_html(), value)
        node = LeafNode(None, value, None)
        self.assertEqual(node.to_html(), value)

    def test_to_str(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")

if __name__ == "__main__":
    unittest.main()
