import re
from  textnode import TextNode
from textnode import text_to_textnodes
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None, alt = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.alt = alt
    
    def TO_HTML(self):
        raise NotImplementedError
    
    def props_to_html(self):
        printout = ""
        if self.props is None:
            return printout
        for key,value in self.props.items():
            printout += f' {key}='
            printout += f'"{value}"'
        return printout
    
    def __repr__(self) -> str:
        return(f" tag={self.tag} value={self.value} children={self.children} props={self.props}")


class LeafNode(HTMLNode):
        def __init__(self, tag=None, value=None, props=None, alt=None):
            super().__init__(tag,value,None,props,alt)
            if value is None:
                raise ValueError
        def __repr__ (self):
            return f"LeafNode({self.tag}, {self.value}, {self.props}, {self.alt})"
                
        def to_html(self):                        
            if self.tag== None:
                    return str(self.value)
            else:
                if self.props is None:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
                else:
                    props_string = ""
                    for key, value in self.props.items():
                        props_string += f" {key}=\"{value}\""
                    return f"<{self.tag}={props_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
     def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children,props)
        if tag is None:
            raise ValueError("No tag provided")
        if children is None or children == []:
            raise ValueError("No children provided")
        
     def to_html(self):
         kids_string = ""
         for kids in self.children:
            kids_string += kids.to_html()
         return f"<{self.tag}> {kids_string} </{self.tag}>"
     
def  text_node_to_html_node(text_node):
    tags = {"text_type_text" : None,
             "text_type_bold" :"b",
             "text_type_italic" :"i",
             "text_type_code" :"code",
             "text_type_link" :"a",
             "text_type_image" :"img"
             }
    if text_node.text_type not in tags:
        raise Exception("Type not compatible")
    if text_node.text_type == "text_type_text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type == "text_type_bold":
        return LeafNode(tags[text_node.text_type], text_node.text)
    elif text_node.text_type == "text_type_italic":
        return LeafNode(tags[text_node.text_type], text_node.text)
    elif text_node.text_type == "text_type_code":
        return LeafNode(tags[text_node.text_type], text_node.text)
    elif text_node.text_type == "text_type_link":
        return LeafNode(tags[text_node.text_type], text_node.text, text_node.url)
    elif text_node.text_type == "text_type_image":
        return LeafNode(tags[text_node.text_type], "", text_node.url, text_node.alt)

def convert_quote_to_html_node(quote_block):
    block_lines = quote_block.split("\n>")
    block_lines[0] = block_lines[0][1:]
    for i in range(len(block_lines)):
        block_lines[i] = block_lines[i].strip()
    return HTMLNode("blockquote", None, text_to_textnodes(block_lines), None, None)

def convert_unorderedlist_to_html_node(quote_block):
    block_lines = quote_block.split("\n-")
    block_lines[0] = block_lines[0][1:]
    children_list = []
    for i in range(len(block_lines)):
        block_lines[i] = block_lines[i].strip()
        children_list.append(TextNode(block_lines[i], None))
    return HTMLNode("ul", None, children_list, None, None)

def convert_orderedlist_to_html_node(quote_block):
    children_list = []
    block_lines = quote_block.split("\n")
    for i in range (0, len(block_lines)):
        if block_lines[i] == '':
            continue
        if block_lines[i][0].isdigit() and block_lines[i][1] == ".":
            block_lines[i] = block_lines[i].strip()
            block_lines[i] = block_lines[i][3:]
            children_list.append(TextNode(block_lines[i], None))
    return HTMLNode("ol", None, children_list, None, None)

def convert_text_to_listitem_node(line):
    if line[0].isdigit() and line[1] == ".":
        line = line.strip()
        line = line[3:]
        text_child = TextNode(line,None)
    if line[0].isdigit() and line[1].isdigit() and line[2] == ".":
        line = line.strip()
        line = line[3:]
        text_child = TextNode(line,None)
    if line.startswith('-'):
        line = line.strip()
        line = line[2:]
        text_child = TextNode(line,None)
    return HTMLNode("li",None,[text_child],None,None)

def convert_code_to_html_node(quote_block):
    if quote_block.startswith('```'):
        quote_block = quote_block[3:-4]
    text_node = TextNode(quote_block.strip(), None)
    code_node = HTMLNode('code', None, [text_node], None, None)
    pre_node = HTMLNode('pre', None, [code_node], None, None)
    return pre_node

def convert_heading_to_html_node(quote_block):
    children_list = []
    one_tag ='#'
    headings = quote_block.split("\n")
    for line in headings:
        line = line.strip()
        for i in range (6, 0, -1):
            if line.startswith(f'{one_tag*i} '):
                line = line[i+1:]
                text_node = TextNode(line, None)
                heading_node = HTMLNode (f'h{i}', None, text_node, None, None)
                children_list.append(heading_node)
                break
    return HTMLNode('headings', None, children_list, None, None)

def convert_paragraph_to_html_node(quote_block):
    text_node =  TextNode(quote_block, None)
    return HTMLNode('p', text_node, None, None, None)
    

def markdown_to_html_node(markdown):
    all_nodes = []
    i = 0
    markdown_lines = markdown.split('\n')
    while i < len(markdown_lines):
        line = markdown_lines[i].strip()
        if line == '':
            i+=1
            continue
        if line.startswith('>'):
            all_nodes.append(convert_quote_to_html_node(line))
            i+=1
        elif re.match("^\s*-",line):
            list_node = HTMLNode("ul",children = [])
            list_item_node = convert_text_to_listitem_node(line)
            list_node.children.append(list_item_node)
            i+= 1
            for line_indices in range(i,len(markdown_lines)):
                if markdown_lines[line_indices] == '':
                    i+=1
                    continue
                if re.match("^s*-",markdown_lines[line_indices]):
                    list_item_node = convert_text_to_listitem_node(markdown_lines[line_indices])
                    list_node.children.append(list_item_node)
                    i+=1
                else:
                    i+=1
                    break
            all_nodes.append(list_node)
        elif line[0] == '1' and line[1] == ".":
            list_node = HTMLNode("ol", children = [])
            list_item_node = convert_text_to_listitem_node(line)
            list_node.children.append(list_item_node)
            i+=1
            for line_indices in range (i,len(markdown_lines)):
                if markdown_lines[line_indices] == '':
                    i+=1
                    continue
                if markdown_lines[line_indices][0].isdigit() and markdown_lines[line_indices][1] == ".":
                    list_item_node =  convert_text_to_listitem_node(markdown_lines[line_indices])
                    list_node.children.append(list_item_node)
                    i+=1
                elif markdown_lines[line_indices][0].isdigit() and markdown_lines[line_indices][1].isdigit() and markdown_lines[line_indices][2] == ".":
                    list_item_node =  convert_text_to_listitem_node(markdown_lines[line_indices])
                    list_node.children.append(list_item_node)
                    i+=1
                else:
                    i+=1
                    break
            all_nodes.append(list_node)
        elif line.startswith('```'):
            code_block = line
            i += 1
            while i < len(markdown_lines):
                code_block += '\n' + markdown_lines[i]
                if re.search("```",markdown_lines[i]):
                    all_nodes.append(convert_code_to_html_node(code_block))
                    i += 1
                    break
                i+=1
        elif line.startswith('#'):
            all_nodes.append(convert_heading_to_html_node(line))
            i+=1
        else:
            all_nodes.append(convert_paragraph_to_html_node(line))
            i+=1
    return all_nodes

def extract_title(markdown):
    markdown_lines = markdown.split('\n')
    for line in markdown_lines:
        if line.startswith('# '):
            line = line.strip()
            line = line[2:]
            return line
    else:
        raise Exception('No h1 header found in file.')
        