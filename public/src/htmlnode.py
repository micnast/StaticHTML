from  textnode import TextNode

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
