from htmlnode import HTMLNode, LeafNode, ParentNode
from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered list"
    O_LIST = "ordered list"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    cleaned_blocks = [block.strip() for block in block_list if block.strip()]
    return cleaned_blocks

def block_to_block_type(markdown_block):
    if (markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))):
        return 'heading'
    if markdown_block.startswith('```') and markdown_block.endswith('```'):
        return 'code'
    if any(line.startswith('> ') for line in markdown_block.split('\n')):
        return 'quote'
    if all(line.startswith(("* ", "- ")) for line in markdown_block.split('\n')):
        return 'unordered list'
    if all(line.strip()[0].isdigit() and line[1] == "." for line in markdown_block.split('\n') if line.strip()):
        return 'ordered list'
    else:
        return 'paragraph'

def markdown_block_to_html_node(markdown_file):
    children_list = []
    markdown_string = ""
    with open(markdown_file, 'r') as f:
        markdown_string = f.read()
    markdown_blocks = markdown_to_blocks(markdown_string)
    for block in markdown_blocks:
        children_list.append(change_block_to_html(block))
    html_node = ParentNode("div",children_list)
    return html_node

def change_block_to_html(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING.value:
        return heading_to_html(block)
    if block_type == BlockType.CODE.value:
        return code_to_html(block)
    if block_type == BlockType.QUOTE.value:
        return quote_to_html(block)
    if block_type == BlockType.U_LIST.value:
        return unordered_list_to_html(block)
    if block_type == BlockType.O_LIST.value:
        return ordered_list_to_html(block)
    if block_type == BlockType.PARAGRAPH.value:
        return paragraph_to_html(block)

def heading_to_html(block):
    split_block = block.split(maxsplit=1)
    header_tag = f"h{split_block[0].count("#")}"
    header_text = split_block[1]
    child_nodes = text_to_children(header_text)
    return ParentNode(header_tag, child_nodes)
    
    
def code_to_html(block):
    child_nodes = text_to_children(block)
    return ParentNode('pre',child_nodes)
    

def quote_to_html(block):
    quote_string = block.replace('> ', '')
    child_nodes = text_to_children(quote_string)
    return ParentNode('blockquote',child_nodes)
    

def unordered_list_to_html(block):
    unordered_list_string = block.split('* ')
    clean_list = list(filter(lambda item: item, unordered_list_string))
    child_nodes = []
    for item in clean_list:
        child_nodes.append(ParentNode("li",text_to_children(item)))
    return ParentNode("ul", child_nodes)
    

def ordered_list_to_html(block):
    split_list = block.split('\n')
    child_nodes = []
    for item in split_list:
        list_number = item[0:2]
        item = item.replace(list_number, '').strip()
        child_nodes.append(ParentNode("li", text_to_children(item)))
    return ParentNode("ol", child_nodes)

def paragraph_to_html(block):
    child_nodes = text_to_children(block)
    return ParentNode("p", child_nodes)


def text_to_children(text):
    leaf_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes


markdown_block_to_html_node('Markdown.md')