import unittest
from inline_markdown import (split_nodes_delimiter,extract_markdown_images,extract_markdown_links,
                             split_nodes_image,split_nodes_links, text_to_textnodes)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_image(self):
        markdown = "This is a text with a ![fish image](https://fish.com)"
        self.assertEqual(extract_markdown_images(markdown), [('fish image','https://fish.com')])

    def test_extract_link(self):
        markdown = "Welcome to the backend camp [to boot dev](https://www.boot.dev)"
        self.assertEqual(extract_markdown_links(markdown), [('to boot dev', 'https://www.boot.dev')])
    
    def test_extract_img_and_link(self):
        markdown = "Hello here we have a ![horrible image](horrible_image.png) and a link to [youtube](https://www.youtube.com)"
        self.assertEqual(extract_markdown_images(markdown),[('horrible image', 'horrible_image.png')])
        self.assertEqual(extract_markdown_links(markdown), [('youtube', 'https://www.youtube.com')])

    def test_node_image_split(self):
        markdown = TextNode("This has a ![dog image](dog.png) do not ignore", TextType.TEXT)
        self.assertEqual([TextNode("This has a ", TextType.TEXT), TextNode("dog image",TextType.IMAGE,"dog.png"), 
                          TextNode(" do not ignore",TextType.TEXT)], split_nodes_image([markdown]))
        
    def test_node_link_split(self):
        markdown = TextNode("This is text has a [youtube link](youtube.com) please click", TextType.TEXT)
        self.assertEqual([TextNode("This is text has a ", TextType.TEXT), TextNode("youtube link",TextType.LINK,"youtube.com"),
                          TextNode(" please click", TextType.TEXT)], split_nodes_links([markdown]))
    def test_node_link_image_split(self):
        markdown = TextNode("This test has an ![image](src/image.png) and also a [link](google.com)", TextType.TEXT)
        self.assertEqual([TextNode("This test has an ", TextType.TEXT),TextNode("image",TextType.IMAGE,"src/image.png"),
                          TextNode(" and also a [link](google.com)", TextType.TEXT)], split_nodes_image([markdown]))
        self.assertEqual([TextNode("This test has an ![image](src/image.png) and also a ", TextType.TEXT),
                          TextNode("link", TextType.LINK, "google.com")],split_nodes_links([markdown]))
    def test_node_no_split(self):
        markdown = TextNode("This text has nothing to be split in", TextType.TEXT)
        self.assertEqual([TextNode("This text has nothing to be split in", TextType.TEXT)], split_nodes_image([markdown]))

    maxDiff = None
    def test_text_to_textnode(self):
        markdown = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ], text_to_textnodes(markdown))
        
    def test_italic_text_to_textnode(self):
        markdown = "This is a *italic* text alone"
        self.assertEqual([TextNode("This is a ", TextType.TEXT), TextNode("italic",TextType.ITALIC), 
                          TextNode(" text alone", TextType.TEXT)], text_to_textnodes(markdown))

    def test_image_to_textnode(self):
        markdown = "This text has an image of ![obi wan image](obi_wan.gif) its cool"
        self.assertEqual([TextNode("This text has an image of ", TextType.TEXT),
                          TextNode("obi wan image", TextType.IMAGE, "obi_wan.gif"), TextNode(" its cool", TextType.TEXT)], 
                          text_to_textnodes(markdown))
        
    def test_no_markdown_text(self):
        markdown = "No special markdown in this text"
        self.assertEqual([TextNode("No special markdown in this text", TextType.TEXT)], text_to_textnodes(markdown))

if __name__ == "__main__":
    unittest.main()