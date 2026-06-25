import re
from enum import Enum
import os
from helpers import markdown_to_blocks, text_to_textnodes
from htmlnode import HTMLNode
from parentnode import ParentNode
from pathlib import Path
from textnode import TextNode, text_node_to_html_node, TextType


HEADING_EXPR: str = r"^#{1,6}"
TITLE_EXPR: str = r"^#\s(.*)?"
CODE_EXPR: str = r"^`{3}\n[^`]*`{3}" 
QUOTE_EXPR: str = r"^>(\s)?"
UNORDERED_LIST_EXPR: str = r"^-\s+"
ORDERED_LIST_EXPR: str = r"^(\d).\s+" 

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    paths: list[str] = os.listdir(dir_path_content)
    if not paths or len(paths) == 0:
        return
    for path in paths:
        joined_path = os.path.join(dir_path_content, path)
        if os.path.isfile(joined_path):
            file_path = Path(path)
            if file_path.suffix != ".md":
                continue
            generate_page(joined_path, 
                          template_path, 
                          os.path.join(dest_dir_path, file_path.with_suffix(".html")))
        else:
            generate_pages_recursive(joined_path, 
                                    template_path, 
                                    os.path.join(dest_dir_path, path))

def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        line = line.strip()
        if line == "":
            continue
        match = re.search(TITLE_EXPR, line)
        if match:
            return match.group(1).strip()
            break # we only check the first non-empty line    
    raise ValueError("no title found at the start of", markdown)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown: str = file.read()
    with open(template_path, 'r') as file:
        template: str = file.read()
    html_node: HTMLNode = markdown_to_html_node(markdown)
    content: str = html_node.to_html()
    title: str = extract_title(markdown)
    page: str = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    basepath: str = os.path.dirname(from_path)
    if basepath != "/":
        basepath += "/"
    page = page.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, 'w') as file:
        file.write(page)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    nodes: list[HTMLNode] = []
    for block in blocks:
        block_type: BlockType = block_to_block_type(block)
        node: HTMLNode = block_to_html_node(block, block_type)
        nodes.append(node)
    return ParentNode("div", nodes)


def block_to_block_type(block: str) -> BlockType:
    block_patterns: list[tuple[str, BlockType]] = [(HEADING_EXPR, BlockType.HEADING),
                                                   (CODE_EXPR, BlockType.CODE)]
    for pattern, block_type in block_patterns:
        match = re.search(pattern, block)
        if match:
            return block_type
     
    # for lists:
    block_parts: list[str] = block.split("\n")
    
    if re.match(QUOTE_EXPR, block):
        for block_part in block_parts:
            if re.match(QUOTE_EXPR, block_part) is None:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    is_valid_list: bool = False
    for block_part in block_parts:
        match = re.match(UNORDERED_LIST_EXPR, block_part)
        is_valid_list = match is not None
        if match is None:
            break

    if is_valid_list:
        return BlockType.UNORDERED_LIST

    current_number: int = 1
    for block_part in block_parts:
        match = re.match(ORDERED_LIST_EXPR, block_part)
        if match:
            if match.groups()[0] == f"{current_number}":
                current_number += 1
                is_valid_list = True
            else:
                is_valid_list = False
                break

    return BlockType.ORDERED_LIST if is_valid_list else BlockType.PARAGRAPH


def block_to_html_node(block: str, block_type: BlockType)-> HTMLNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return markdown_paragraph_to_node(block)
        case BlockType.HEADING:
            return markdown_header_to_node(block)
        case BlockType.CODE:
            return markdown_code_to_node(block)
        case BlockType.QUOTE:
            return markdown_quote_to_node(block)
        case BlockType.UNORDERED_LIST:
            return markdown_list_to_node(block, is_ordered = False)
        case BlockType.ORDERED_LIST:
            return markdown_list_to_node(block, is_ordered = True)
        case _:
            raise Exception(f"BlockType \"{block_type}\" not known")


def markdown_paragraph_to_node(paragraph: str) -> HTMLNode:
    paragraph_text: str = re.sub(r"\n{1,}", " ", paragraph)
    return ParentNode("p", text_to_children(paragraph_text))


def markdown_header_to_node(header: str) -> HTMLNode:
    match = re.match(HEADING_EXPR, header)
    matches: int = match.span()[1]
    return ParentNode(f"h{matches}", text_to_children(re.sub(match.re, "", header).strip()))


def markdown_code_to_node(code: str) -> HTMLNode:
    code_text: str = code.lstrip("```\n").rstrip("```")
    raw_text_node: TextNode = TextNode(code_text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code_node: ParentNode = ParentNode("code", [child])
    return ParentNode("pre", [code_node])


def markdown_quote_to_node(quote: str) -> HTMLNode:
    quote_text: str = re.sub(r"\n{1,}", " ", re.sub(r">(\s)?", "", quote))
    return ParentNode("blockquote", text_to_children(quote_text))


def markdown_list_to_node(text: str, is_ordered:bool) -> HTMLNode:
    expression: str = ""
    tag: str = ""
    if is_ordered:
        expression = ORDERED_LIST_EXPR
        tag = "ol"
    else:
        expression = UNORDERED_LIST_EXPR
        tag = "ul"
    text_parts: list[str] = text.split("\n")
    item_list: list[HTMLNode] = []
    for part in text_parts:
        item_text: str = re.sub(expression, "", part)
        item_list.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode(tag, item_list)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] =  text_to_textnodes(text)
    children: list[HTMLNode] = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

    
