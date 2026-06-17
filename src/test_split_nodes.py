import unittest
from textnode import TextNode, TextType
from helpers import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, 
                             [
                                 TextNode("This is text with a ", TextType.TEXT),
                                 TextNode("code block", TextType.CODE),
                                 TextNode(" word", TextType.TEXT)
                             ])

    def test_double_type(self):
        node = TextNode("This is text with a first `code example 1` and a second `code example 2` in text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes,
                            [
                                TextNode("This is text with a first ", TextType.TEXT),
                                TextNode("code example 1", TextType.CODE),
                                TextNode(" and a second ", TextType.TEXT),
                                TextNode("code example 2", TextType.CODE),
                                TextNode(" in text", TextType.TEXT)\
                            ])

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

    def test_no_value_left_as_text(self):
        node = TextNode("This is a text that contains no md TextTypes", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

if __name__ == "__main__":
    unittest.main()
