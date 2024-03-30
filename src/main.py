from textnode import TextNode
import os
import shutil
from generatepage import generate_page
from generatepage import generate_pages_recursive


static_dir = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/src/static'
public_dir = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/src/public'
index_md_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/content'
template_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public/template.html'
destination_path = '/home/micnast/WORKSPACE/BootDevProjects/github/micnast/StaticHTML/public'

def  main():
    generate_pages_recursive(index_md_path, template_path, destination_path)

main()