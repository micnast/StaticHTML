import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        props_practice = {"banana": "yellow",
                          "Blueberry": "blue"}
        node = HTMLNode(None, None, None, props_practice)
        target_answer = str(' banana="yellow" Blueberry="blue"')
        self.assertEqual(node.props_to_html(), target_answer)
        
       
node_test_1 = LeafNode("p", "This is a paragraph of text.")
print(node_test_1.to_html())
node_test_2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
print(node_test_2.to_html())
node_test_3 = LeafNode("b", "This is a profound quote, says I.", {"href": "https://www.google.com", "click": "you got bananas"})
print(node_test_3.to_html())
        

if __name__ == "__main__":
    unittest.main()