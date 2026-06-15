import unittest
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_double_type(self):
        node = TextNode("This is text with a first `code example 1` and a second `code example 2` in text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is text with a first ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code example 1", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" and a second ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("code example 2", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode(" in text", TextType.TEXT))

    def test_text_node(self):
        node = TextNode("This is an italic block", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)
        
    def test_error_no_nodes(self):
        none_node_func = lambda : split_nodes_delimiter(None, "`", TextType.CODE)
        empty_nodes_list_func = lambda : split_nodes_delimiter([], "`", TextType.CODE)
        self.assertRaises(ValueError, none_node_func)
        self.assertRaises(ValueError, empty_nodes_list_func)
    
    def test_error_unmatched_delimiters(self):
        node = TextNode("This is text with an unmatched `code block", TextType.TEXT)
        unmatched_func =  lambda : split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertRaises(SyntaxError, unmatched_func)


if __name__ == "__main__":
    unittest.main()
