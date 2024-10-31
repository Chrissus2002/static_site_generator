import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq_italic(self):
        node = TextNode("This node is italic", TextType.ITALIC)
        node2 = TextNode("This node is italic", TextType.ITALIC)
        self.assertEqual(node,node2)
    def test_eq_code(self):
        node = TextNode("This node is code", TextType.CODE)
        node2 = TextNode("This node is code", TextType.CODE)
        self.assertEqual(node,node2)
    def test_eq_url(self):
        node = TextNode("This has a URL", TextType.LINK, "Boot.dev")
        node2 = TextNode("This has a URL", TextType.LINK, "Boot.dev")
        self.assertEqual(node,node2)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("raw text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "raw text")
    def test_bold_text_to_html(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>bold text</b>")
    def test_image_to_html_node(self):
        node = TextNode("random image", TextType.IMAGE, "src/image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<img src=\"src/image\" alt=\"random image\"></img>")



if __name__ == "__main__":
    unittest.main()