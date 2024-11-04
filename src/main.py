from block_markdown import markdown_to_html_node
import os, shutil

def copy_src_dir_to_dest_dir(src_dir = './static', dest_dir = './public'):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    for file in os.listdir(src_dir):
        src_full_path = os.path.join(src_dir, file)
        dest_full_path = os.path.join(dest_dir, file)
        if os.path.isfile(src_full_path):
            shutil.copy(src_full_path, dest_dir)
        elif os.path.isdir(src_full_path):
            os.mkdir(dest_full_path)
            copy_src_dir_to_dest_dir(src_full_path,dest_full_path)
    
def extract_title(markdown):
    title = None
    markdown_list = markdown.split('\n')
    for line in markdown_list:
        if line.startswith('# '):
            title_list = line.split('# ')
            clean_title_list = [line for line in title_list if line.strip()]
            title = clean_title_list[0].strip()
    if title == None:
        raise Exception("Invalid markdown, there is no h1 for the title")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f'Generating a page from {from_path} to {dest_path} using {template_path}')

    #From path file creation
    from_file_path = os.path.join(from_path, 'index.md')
    markdown_file = open(from_file_path, 'r').read()

    #changing the template and writing it somewhere else
    template_file = open(template_path, 'r').read()
    converted_node = markdown_to_html_node(markdown_file)
    title = extract_title(markdown_file)
    template_file = template_file.replace('{{ Title }}', title)
    template_file = template_file.replace('{{ Content }}', converted_node.to_html())

    #destination path file
    os.makedirs(dest_path, exist_ok=True)
    dest_file_path = os.path.join(dest_path, 'index.html')
    with open(dest_file_path, 'w') as full_html_file:
        full_html_file.write(template_file)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        from_file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(from_file_path):
            generate_page(os.path.dirname(from_file_path), template_path, dest_dir_path)
        elif os.path.isdir(from_file_path): 
            destination_path_file = os.path.join(dest_dir_path, file)
            generate_pages_recursive(from_file_path, template_path, destination_path_file)
        

def main():
    copy_src_dir_to_dest_dir()
    generate_pages_recursive('./content', './template.html', './public')


if __name__ == "__main__":
    main()