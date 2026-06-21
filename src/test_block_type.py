import unittest
from markdown import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):

    def test_valid_heading(self):
        block: str = "## This is a subtitle"
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_valid_code(self):
        block: str = """```
        This is a code block
        ```"""
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)
        
    def test_valid_quote(self):
        block: str = """> This is a quote \n> this too"""
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)
         
    def test_valid_unordered_list(self):
        block: str = "- This is a point in an unordered  list"
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)
          
    def test_valid_ordered_list(self):
        block: str = """1. This is a first point
        2. This is a second point
        3. ... and a third one
        """
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)
           
    def test_valid_paragraph(self):
        block: str = "This is a normal text"
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
         
    def test_invalid_code(self):
        block: str = """```
        This is no code"""
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_ordered_list(self):
        block: str = """1. This is a first point
        3. This is a second point
        3. ... and a third one
        """
        block_type: BlockType = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)    
if __name__ == "__main__":
    unittest.main()
