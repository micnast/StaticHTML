from htmlnode import markdown_to_html_node
from htmlnode import ParentNode
from htmlnode import extract_title
from htmlnode import LeafNode
import os



index_md_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/content/index.md'
template_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/template.html'
destination_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/index.html'



def generate_page(from_path, template_path, dest_path):
    print (f'Generating page from {from_path} to {dest_path} using {template_path}.')
    with open(from_path, 'r') as file:
        markdown_file = file.read()
    with open(template_path, 'r') as t_file:
        template_file = t_file.read()
    title = extract_title(markdown_file)
    html_nodes = markdown_to_html_node(markdown_file)
    final = ''
    for node in html_nodes.children:
        if isinstance(node, list):
            for subnode in node:
                if isinstance(subnode, (ParentNode,LeafNode)):
                    final += subnode.to_html()
        elif isinstance(node, (ParentNode, LeafNode)):
            final += node.to_html()
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", final)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as template_html:
        template_html.write(template_file)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f'Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}')
    with open(dir_path_content, 'r') as file:
        
        
        if os.path.isfile(dir_path_content) and file.name.endswith('.md'):
            markdown_file = file.read()


generate_page(index_md_path, template_path, destination_path)
