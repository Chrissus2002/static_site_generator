from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #New list to add the TextType
    new_nodes = []
    #Look through the list of old nodes to seperate the text
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        split_node = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("Invalid markdown: formated section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_node.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_node)
    return new_nodes


def extract_markdown_images(text):
    image_list = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return image_list


def extract_markdown_links(text):
    link_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return link_list


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        image_list = extract_markdown_images(node.text)
        if len(image_list) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for i in image_list:
            image_alt = i[0]
            image_url = i[1]
            sections = original_text.split(f"![{image_alt}]({image_url})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section was not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE,image_url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text,TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        link_list = extract_markdown_links(node.text)
        if len(link_list) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for i in link_list:
            link_alt = i[0]
            link_url = i[1]
            sections = original_text.split(f"[{link_alt}]({link_url})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section was not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK,link_url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text,TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    output_list = []
    split_bold = split_nodes_delimiter(nodes, "**",TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "*",TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`",TextType.CODE)
    split_image = split_nodes_image(split_code)
    split_node = split_nodes_links(split_image)
    output_list.extend(split_node)
    return output_list

