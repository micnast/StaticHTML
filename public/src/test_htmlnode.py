import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextNode
from htmlnode import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        props_practice = {"banana": "yellow",
                          "Blueberry": "blue"}
        node = HTMLNode(None, None, None, props_practice)
        target_answer = str(' banana="yellow" Blueberry="blue"')
        self.assertEqual(node.props_to_html(), target_answer)
        
test_text_node = TextNode("this is my fun text", "text_type_italic")
test_image_node = TextNode("this is a hilarious meme", "text_type_image", "wwww.google.com","this is hilarious" )
node_inside = LeafNode("p", "get me out of here", None)
middle_parent = ParentNode("z", [node_inside], None)
node = ParentNode(
    "p",
    [
        ParentNode("x", [middle_parent], None),
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

print(node.to_html()) 
print(text_node_to_html_node(test_text_node))
print(text_node_to_html_node(test_image_node))


if __name__ == "__main__":
    unittest.main()