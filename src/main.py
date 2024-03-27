from textnode import TextNode
import os
import shutil
from generatepage import generate_page

static_dir = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/src/static'
public_dir = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/src/public'
index_md_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/content/index.md'
template_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/template.html'
destination_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/index.html'

def  main():
    generate_page(index_md_path, template_path, destination_path)

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
    
main()