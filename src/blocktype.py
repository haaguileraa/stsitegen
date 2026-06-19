import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    block_patterns: list[tuple[str, BlockType]] = [(r"^#{1,6}", BlockType.HEADING),
                                                   (r"^`{3}\n[^`]*`{3}", BlockType.CODE),
                                                   (r"^>[^>]*>", BlockType.QUOTE),
                                                   (r"^-\s+", BlockType.UNORDERED_LIST)]
    for pattern, block_type in block_patterns:
        match = re.search(pattern, block)
        if match:
            return block_type
     
    # for ordered lists:
    block_parts: list[str] = block.split("\n")
    pattern: str = r"^(\d).\s+"
    current_number: int = 1
    is_valid_ordered_list: bool = False
    for block_part in block_parts:
        match = re.match(pattern, block_part)
        if match:
            if match.groups()[0] == f"{current_number}":
                current_number += 1
                is_valid_ordered_list = True
            else:
                is_valid_ordered_list = False
                break

    return BlockType.ORDERED_LIST if is_valid_ordered_list else BlockType.PARAGRAPH

    
 
