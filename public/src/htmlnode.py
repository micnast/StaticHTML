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


"""
convert_quote_to_html_node(quote_block)
convert_unordered_list_to_html_node(unordered_list_block)
convert_ordered_list_to_html_node(ordered_list_block)
convert_code_to_html_node(code_block)
convert_heading_to_html_node(heading_block)
convert_paragraph_to_html_node(paragraph_block)
And then, you'll have your larger orchestrating function that utilizes the above functions:

markdown_to_html_node(markdown)
"""

quote = """- Wake up
- Brush teeth
- Shower
- Get dressed
- Eat breakfast
"""


def convert_quote_to_html_node(quote_block):
    block_lines = quote_block.split("\n>")
    block_lines[0] = block_lines[0][1:]
    for i in range(len(block_lines)):
        block_lines[i] = block_lines[i].strip()
    return HTMLNode("blockquote", None, text_to_textnodes(block_lines), None, None)

def convert_unorderedlist_to_html_node(quote_block):
    block_lines = quote_block.split("\n>")
    children_list = []
    for i in range(len(block_lines)):
        block_lines[i] = block_lines[i].strip()
        block_lines[i] = block_lines[i][2:]
        children_list.append(TextNode(block_lines, any))
    return HTMLNode("li", None, children_list, None, None)


print(convert_unorderedlist_to_html_node(quote))