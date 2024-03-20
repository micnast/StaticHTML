from htmlnode import markdown_to_html_node
from htmlnode import ParentNode
from htmlnode import extract_title
import os


def generate_page(from_path, template_path, dest_path):
    print (f'Generating page from {from_path} to {dest_path} using {template_path}.')
    with open(from_path, 'r') as file:
        markdown_file = file.read()
    with open(template_path, 'r') as t_file:
        template_file = t_file.read()
    title = extract_title(markdown_file)
    html_nodes = markdown_to_html_node(markdown_file)
    final = html_nodes.to_html()
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", final)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as template_html:
        template_html.write(template_file)
