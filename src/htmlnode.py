import re
from  textnode import TextNode
from textnode import text_to_textnodes
from textnode import block_to_block_type
from textnode import markdown_to_blocks


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None, alt = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.alt = alt
    
    def to_html(self):
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
                print("EMPTY tags cause THIS")
                return str(self.value)
            if self.value == None:
                print("Empty values in LeafNodes cause this")
                return ""
            if self.tag == '':
                return f"{self.value}"
            else:
                if self.props is None:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
                if isinstance (self.props, str):
                    return f"<{self.tag} href={self.props}>{self.value}</{self.tag}>"
                if isinstance (self.props, dict):
                    props_string = ""
                    for key, value in self.props.items():
                        props_string += f" {key}=\"{value}\""
                    return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
     def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children,props)
        if tag is None:
            raise ValueError("No tag provided")
        
     def to_html(self):
         kids_string = ""
         if self.children is None or not self.children:
            raise ValueError("Cannot render HTML. No children present in the ParentNode.")
         for kids in self.children:
            if isinstance(kids, str):
                kids_string += kids
            elif isinstance(kids, list):
                for baby in kids:
                    kids_string += baby.to_html()
            else:
                kids_string += kids.to_html()
         html_code = f"<{self.tag}>{kids_string}</{self.tag}>"
         return html_code



def  convert_text_node_to_html_node(text_node):
    node_list = []
    tags = {'p':'p',
             'text':'p',
             "b" :"b",
             "i" :"i",
             "code" :"code",
             "a" :"a",
             "image" :"image",
             'h1': 'h1',
             'h2': 'h2',
             'h3': 'h3',
             'h4': 'h4',
             'h5': 'h5',
             'h6': 'h6',
             '': 'plain'
             }
    if isinstance(text_node,list):
        for node in text_node:
            if node.text_type == '':
                node_list.append(LeafNode('', node.text))
            if node.text_type not in tags:
                raise Exception(f"Type {node.text_type} not compatible")
            if node.text_type == "p" or node.text_type == 'text':
                node_list.append(LeafNode('p', node.text))
            elif node.text_type == "b":
                node_list.append(LeafNode(tags[node.text_type], node.text))
            elif node.text_type == "i":
                node_list.append(LeafNode(tags[node.text_type], node.text))
            elif node.text_type == "code":
                node_list.append(LeafNode(tags[node.text_type], node.text))
            elif node.text_type == "a":
                props_dict = {'href': node.url}
                node_list.append(LeafNode(tags[node.text_type], node.text, props_dict))
            elif node.text_type == "image":
                node_list.append(LeafNode(tags[node.text_type], "", node.url, node.alt))
        return node_list
    else:
        if text_node.text == '':
            return
        if text_node.text_type not in tags:
            raise Exception(f"Type {text_node.text_type} not compatible")
        if text_node.text_type == "p" or text_node.text_type == 'text':
            return LeafNode(text_node.text_type, text_node.text)
        elif text_node.text_type == "b":
            return LeafNode(tags[text_node.text_type], text_node.text)
        elif text_node.text_type == "i":
            return LeafNode(tags[text_node.text_type], text_node.text)
        elif text_node.text_type == "code":
            return LeafNode(tags[text_node.text_type], text_node.text)
        elif text_node.text_type == "a":
            props_dict = {'href': text_node.url}
            return LeafNode(tags[text_node.text_type], text_node.text, props_dict)
        elif text_node.text_type == "image":
            return LeafNode(tags[text_node.text_type], "", text_node.url, text_node.alt)

def convert_quote_to_html_node(quote_block):
    block_lines = quote_block.split("\n>")
    block_lines[0] = block_lines[0][1:]
    for i in range(len(block_lines)):
        block_lines[i] = block_lines[i].strip()
    return ParentNode("quote", block_lines, None)

def convert_unorderedlist_to_html_node(quote_block):
    block_lines = quote_block.split("\n-")
    block_lines[0] = block_lines[0][1:]
    children_list = []
    for i in range(len(block_lines)):
        block_lines[i] = block_lines[i].strip()
        children_list.append(LeafNode('li', block_lines[i]))
    return ParentNode("ul", children_list, None)

def convert_orderedlist_to_html_node(quote_block):
    children_list = []
    block_lines = quote_block.split("\n")
    for i in range (0, len(block_lines)):
        if block_lines[i] == '':
            continue
        if block_lines[i][0].isdigit() and block_lines[i][1] == ".":
            block_lines[i] = block_lines[i].strip()
            block_lines[i] = block_lines[i][3:]
            children_list.append(LeafNode('li', block_lines[i]))
    return ParentNode("ol", children_list, None)

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
    return LeafNode("li",text_child.text,None,None)

def convert_code_to_html_node(quote_block):
    if quote_block.startswith('```'):
        quote_block = quote_block[3:-4]
    code_node = LeafNode('code', quote_block.strip(), None, None)
    pre_node = ParentNode('pre', [code_node], None)
    return pre_node

def convert_heading_to_html_node(quote_block):
    children_list = []
    one_tag ='#'
    headings = quote_block.split("\n")
    for line in headings:
        line = line.strip()
        for i in range (6, 0, -1):
            if line.startswith(f'{one_tag*i} '):
                heading_tag =  f'h{i}'
                line = line[i+1:]
                text_node = TextNode(line, heading_tag)
                parent_heading_node = ParentNode (text_node.text_type,text_to_textnodes(text_node.text), None)
                for textnode in parent_heading_node.children:
                    if textnode.text_type == 'a':
                        textnode.text_type = ''
                parent_heading_node.children = convert_text_node_to_html_node(parent_heading_node.children)
                children_list.append(parent_heading_node)
                break
    return parent_heading_node

def text_to_children(text):
    text_nodes =  text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = convert_text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def convert_paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode('p', children)
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == 'p':
        return convert_paragraph_to_html_node(block)
    if block_type == 'heading':
        return convert_heading_to_html_node(block)
    if block_type == 'code':
        converted_code_block =  convert_code_to_html_node(block)
        return converted_code_block
    if block_type == 'ol':
        return convert_orderedlist_to_html_node(block)
    if block_type == 'ul':
        return convert_unorderedlist_to_html_node(block)
    if block_type == 'quote':
        return convert_quote_to_html_node(block)
    else:
        raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        print(block,'-----------------------')
        html_node = block_to_html_node(block)
        children.append(html_node)
        print(html_node)
    return ParentNode("div", children, None)

def extract_title(markdown):
    markdown_lines = markdown.split('\n')
    for line in markdown_lines:
        if line.startswith('# '):
            line = line.strip()
            line = line[2:]
            return line
    else:
        raise Exception('No h1 header found in file.')



example_short = '''# Tolkien Fan Club

I like Tolkien. Read my [first post here](/majesty)
'''

markdown_to_html_node(example_short)


example = """# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**

### Crafting Middle-earth
Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

## Themes of *Timeless* Relevance

### The *Struggle* of Good vs. Evil

At its heart, *The Lord of the Rings* is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

- The resilience of the human (and hobbit) spirit in the face of overwhelming odds
- The corrupting influence of power, epitomized by the One Ring
- The importance of friendship, loyalty, and sacrifice

These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

## A Legacy **Unmatched**

### The Influence on Modern Fantasy

The shadow that *The Lord of the Rings* casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

- The archetypal "hero's journey" that has become a staple of fantasy narratives
- The trope of the "fellowship," a diverse group banding together to face a common foe
- The concept of a richly detailed fantasy world, which has become a benchmark for the genre

## Conclusion

As we stand at the threshold of this mystical realm, it is clear that *The Lord of the Rings* is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: *The Lord of the Rings* reigns supreme as the greatest legendarium our world has ever known.

Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all.
"""
