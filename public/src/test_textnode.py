import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_init(self):
        text = "something"
        text_type = 'underlined bitches'
        node = TextNode(text, text_type, None)
        self.assertIsNone(node.url)
    
    def test_uneq(self):
        text1 = "bananas"
        text2 = "bingo"
        text_type = "hello world"
        url = None
        node1 = TextNode(text1, text_type, url)
        node2 = TextNode(text2, text_type, url)
        self.assertNotEqual(node1, node2)



    
    
        

if __name__ == "__main__":
    unittest.main()
