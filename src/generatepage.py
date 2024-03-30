from htmlnode import markdown_to_html_node
from htmlnode import ParentNode
from htmlnode import extract_title
from htmlnode import LeafNode
import os



index_md_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/content'
template_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/template.html'
destination_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public'

def move_dir(from_dir, to_dir, copied_files = None):
    if copied_files is None:
        copied_files = {}
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    file_list = os.listdir(from_dir)
    for file in file_list:
        if os.path.isfile(os.path.join(from_dir, file)):
            src_path = os.path.join(from_dir, file)
            dst_path = os.path.join(to_dir, file)
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.copy(src_path, dst_path)
            copied_files[src_path] = dst_path
    for directory in file_list:
        if os.path.isdir(os.path.join(from_dir, directory)):
            src_dir_path = os.path.join(from_dir, directory)
            dst_dir_path = os.path.join(to_dir, directory)
            if os.path.exists(dst_dir_path):
                shutil.rmtree(dst_dir_path)
            copied_files[src_dir_path] = dst_dir_path
            move_dir(src_dir_path, dst_dir_path, copied_files) 
    with open('copy_log.txt', 'w') as log_file:
        for src,dst in copied_files.items():
            log_file.write(f"Copied from {src} to {dst}\n")


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
    with open(template_path, 'r') as t_file:
        template_file = t_file.read()
    file_list = os.listdir(dir_path_content)
    for item in file_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith('.md'):
            with open(item_path, 'r') as markdown_path:
                markdown_file = markdown_path.read()
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
                current_template = template_file.replace("{{ Title }}", title)
                current_template = current_template.replace("{{ Content }}", final)
                os.makedirs(dest_dir_path, exist_ok=True)
                with open(os.path.join(dest_dir_path, f'{os.path.splitext(item)[0]}.html'), 'w') as current_template_html:
                    current_template_html.write(current_template)
        elif os.path.isdir(item_path):
            relative_path = os.path.relpath(item_path, start=dir_path_content)
            new_dest_path = os.path.join(dest_dir_path, relative_path)
            generate_pages_recursive(item_path, template_path, new_dest_path)

generate_pages_recursive(index_md_path, template_path, destination_path)
