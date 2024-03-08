class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
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
        def __init__(self, tag=None, value=None, props=None):
            super().__init__(tag,value,None,props)
            if value is None:
                raise ValueError
                
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