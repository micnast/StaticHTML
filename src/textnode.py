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


text_type_bold = 'b'       
text_type_italic = 'i'
text_type_code = 'code'
text_type_text = 'text'
text_type_link = 'a'
text_type_image = 'image'

delimiter_keys = {'**':text_type_bold,
                        '*':text_type_italic,
                        '`':text_type_code, 
                    }

old_text_node1 = TextNode('this is the text', text_type_text)
old_text_node2 = TextNode('this is a `quote part` of the text', text_type_text)
old_text_node3 = TextNode('`code part here` then **bold part** text.', text_type_text)
list_of_nodes = [old_text_node1 , old_text_node2, old_text_node3]
example_short = '''Once upon a time, in a **faraway land**, there lived a wise old bear named Boots. Boots was not an ordinary bear; he was an *augmentus*, a magical bear with the ability to speak and wield magic. 

`Boots loved two things above all: teaching and honey.` Every day, he would wander the forest, sharing his knowledge with the animals, teaching them the secrets of the magical arts. 

One day, while exploring a *hidden glade*, Boots stumbled upon a **mysterious artifact**. This artifact, a **golden comb**, was said to produce the sweetest honey in the world. Boots knew that with this comb, he could make the forest a **better**'''

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    counter = 0
    if isinstance(old_nodes, list):
        for node in old_nodes:
            if isinstance(node, TextNode) and node.text_type != 'text':
                new_nodes.append(node)
            if isinstance(node, TextNode) and node.text_type == 'text':        
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
    if isinstance(old_nodes, str):
        counter = 0
        split_text_list = old_nodes.split(delimiter)
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
                        leftover = []
                        continue
                    else:
                        new_nodes.append(TextNode(leftover[0], node.text_type, node.url, node.alt))
                        leftover=[]
                        continue
                else:
                    split_text_list = leftover[0].split(f"![{image_tup[0][0]}]({image_tup[0][1]})",1)
                    new_nodes.append(TextNode(split_text_list[0], node.text_type))
                    new_nodes.append(TextNode(image_tup[0][0], "image", f'"{image_tup[0][1]}"'))
                    leftover=[]
                    leftover.append(split_text_list[1])
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        if isinstance(node, TextNode):
            if node.text_type != 'text':
                new_nodes.append(node)
            else:
                leftover = [node.text]
                while len(leftover)==1:
                    link_tup = extract_markdown_links(leftover[0])
                    if link_tup == []:
                        if leftover == ['']:
                            leftover = []
                            continue
                        else:
                            new_nodes.append(TextNode(leftover[0], 'a', node.url, node.alt))
                            leftover = []
                            continue
                    else:
                        split_text_list = leftover[0].split(f"[{link_tup[0][0]}]({link_tup[0][1]})",1)
                        if split_text_list[0].strip():
                            new_nodes.append(TextNode(split_text_list[0],'p'))
                        new_nodes.append(TextNode(link_tup[0][0], 'a', f'{link_tup[0][1]}'))
                        leftover = []
                        leftover.append(split_text_list[1])
    return new_nodes

def text_to_textnodes(node_list):
    delimiter_bold = split_nodes_delimiter(node_list,'**', text_type_bold)
    delimiter_italic = split_nodes_delimiter(delimiter_bold,'*', text_type_italic)
    delimiter_code = split_nodes_delimiter(delimiter_italic,'`', text_type_code)
    split_image = split_nodes_image(delimiter_code)
    final_split_link = split_nodes_link(split_image)
    return final_split_link

def markdown_to_blocks(markdown):
    markdown_list = markdown.split("\n\n")
    for i in range(len(markdown_list)):
        markdown_list[i] = markdown_list[i].strip()
    return(markdown_list)

def block_to_block_type(block):
    block_type_paragraph = "p"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_unordered_list = "ul"
    block_type_ordered_list = "ol"
    if block.startswith("#"):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif block.startswith(">"):
        block_lines = block.split("\n")
        for i in range(len(block_lines)):
            block_lines[i]= block_lines[i].strip()
            if block_lines[i].startswith(">") == False:
                    return block_type_paragraph
        else:
            return block_type_quote
    elif block.startswith("*") or block.startswith("-"):
        block_lines = block.split("\n")
        for i  in range(len(block_lines)):
            block_lines[i] = block_lines[i].strip()
            if block_lines[i].startswith("*") == False and block_lines[i].startswith("-") == False:
                return block_type_paragraph
        else:
            return block_type_unordered_list
    elif block.startswith("1."):
        block_lines = block.split("\n")
        for i in range(len(block_lines)):
            if not block_lines[i][0].isdigit() or not block_lines[i][1] == "." or not block_lines[i][2] == " ":
                return block_type_paragraph
        else:
            return block_type_ordered_list
    else:
        return block_type_paragraph