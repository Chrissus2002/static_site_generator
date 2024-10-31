from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url
    def __eq__(self,other):
        if self.text ==  other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type},{self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT.value:
        no_tag_node = LeafNode(None,text_node.text)
        return no_tag_node
    if text_node.text_type == TextType.BOLD.value:
        bold_text_node = LeafNode("b", text_node.text)
        return bold_text_node
    if text_node.text_type == TextType.ITALIC.value:
        italic_text_node = LeafNode("i",text_node.text)
        return italic_text_node
    if text_node.text_type == TextType.CODE.value:
        code_text_node = LeafNode("code", text_node.text)
        return code_text_node
    if text_node.text_type == TextType.LINK.value:
        link_text_node = LeafNode("a", text_node.text, {"href":text_node.url})
        return link_text_node
    if text_node.text_type == TextType.IMAGE.value:
        image_text_node = LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
        return image_text_node
    else:
        raise Exception(f"Text type is invalid: {text_node.text_type} is not valid")