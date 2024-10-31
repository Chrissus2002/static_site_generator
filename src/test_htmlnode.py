import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Hello page", ["a"], {"bold":"True"})
        node2 = HTMLNode("p", "Hello page", ["a"], {"bold":"True"})
        self.assertEqual(node,node2)
    def test_list(self):
        node = HTMLNode("a", "Click me", props={"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("a", "Click me", props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node,node2)
    def test_none(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node,node2)

    def test_leaf_no_chilren(self):
        node = LeafNode("a", "Click me", {"href":"google.com"})
        self.assertEqual(node.to_html(), '<a href="google.com">Click me</a>')
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_parent_children(self):
        node = ParentNode("p", [LeafNode("b","Bold Text"), LeafNode("a","Link Text", {"href":"youtube.com"}), 
                                LeafNode(None, value="Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold Text</b><a href=\"youtube.com\">Link Text</a>Normal text</p>")
    def test_parent_in_parent(self):
        node = ParentNode("div",[ParentNode("p", [LeafNode("b","bold text"), LeafNode("h1", "Heading 1"), 
                                                           LeafNode(None,"Normal text")])])
        self.assertEqual(node.to_html(), "<div><p><b>bold text</b><h1>Heading 1</h1>Normal text</p></div>")
    

if __name__ == "__main__":
    unittest.main()
