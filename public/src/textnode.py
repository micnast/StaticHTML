import re

class TextNode:
    def __init__(self, text, text_type, url = None, alt = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.alt = alt

    def __eq__ (self, other):
        return (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url)

    def __repr__ (self):
        return f"TextNode({self.text}, {self.text_type}, {self.url}, {self.alt})"


text_type_bold = 'bold'       
text_type_italic = 'italic'
text_type_code = 'code'
text_type_text = 'text'
text_type_link = 'link'
text_type_image = 'image'

delimiter_keys = {'**':text_type_bold,
                        '*':text_type_italic,
                        '`':text_type_code, 
                    }

old_text_node1 = TextNode('this is the text', text_type_text)
old_text_node2 = TextNode('this is a `quote part` of the text', text_type_text)
old_text_node3 = TextNode('`code part here` then normal text.', text_type_text)
list_of_nodes = [old_text_node1 , old_text_node2, old_text_node3]

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    counter = 0
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        if isinstance(node, TextNode):
            if node.text_type != text_type_text:
                new_nodes.append(node)
                continue
            else:
                counter = 0
                split_text_list = node.text.split(delimiter)
                for section in split_text_list:
                    counter +=1
                    if section =='':
                        continue
                    if counter % 2 != 0:
                        new_nodes.append(TextNode(section, text_type_text))
                    else:
                       new_nodes.append(TextNode(section, text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return (matches)

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        if isinstance(node, TextNode):
            leftover = [node.text]
            while len(leftover)==1:
                image_tup = extract_markdown_images(leftover[0])
                if image_tup == []:
                    if leftover == ['']:
                        leftover == []
                        continue
                    else:
                        new_nodes.append(TextNode(leftover[0], node.text_type, node.url, node.alt))
                        leftover=[]
                        continue
                else:
                    split_text_list = leftover[0].split(f"![{image_tup[0][0]}]({image_tup[0][1]})",1)
                    new_nodes.append(TextNode(split_text_list[0], node.text_type))
                    new_nodes.append(TextNode(image_tup[0][0], "text_type_image", f'"{image_tup[0][1]}"'))
                    leftover=[]
                    leftover.append(split_text_list[1])
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        if isinstance(node, TextNode):
            leftover = [node.text]
            while len(leftover)==1:
                link_tup = extract_markdown_links(leftover[0])
                if link_tup == []:
                    if leftover == ['']:
                        leftover = []
                        continue
                    else:
                        new_nodes.append(TextNode(leftover[0], node.text_type, node.url, node.alt))
                        leftover = []
                        continue
                else:
                    split_text_list = leftover[0].split(f"[{link_tup[0][0]}]({link_tup[0][1]})",1)
                    new_nodes.append(TextNode(split_text_list[0], node.text_type))
                    new_nodes.append(TextNode(link_tup[0][0], "text_type_link", f'"{link_tup[0][1]}"'))
                    leftover = []
                    leftover.append(split_text_list[1])
    return new_nodes

def text_to_textnodes(node_list):
    split_link_nodes = []
    split_delimeter_nodes = []
    delimiter_bold = split_nodes_delimiter(node_list,'**', text_type_bold)
    delimiter_italic = split_nodes_delimiter(delimiter_bold,'*', text_type_italic)
    delimiter_code = split_nodes_delimiter(delimiter_italic,'`', text_type_code)
    split_image = split_nodes_image(delimiter_code)
    split_link = split_nodes_link(split_image)
    return split_link
    
    
    


# Do the delimiter last cos it wants to go through a list of nodes anyway. 


test_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
node_complete = TextNode(
    "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
    text_type_text, None, None)
node_list = [node_complete]


print(text_to_textnodes(node_list))
