import os

def absolute_path(simple_path: str) -> str:
    print("Inside absolute_path, the path to the currently executing python script is: ")
    this_file_realpath = os.path.realpath(__file__)
    print(this_file_realpath)

    parent_dir = os.path.dirname(this_file_realpath)
    absolute_path = os.path.join(parent_dir, simple_path)
    print("Got absolute_path: ")
    print(absolute_path)
    return absolute_path


def ensure_storage_directory(simple_container_dir: str, counter_filename: str, storage_dir: str):
    print("Inside file_storage_utils, the ensure_storage_directory function, about to use absolute_path...")
    container_dir = absolute_path(simple_container_dir)
    # counter_filename = absolute_path(simple_counter_filename)
    try:    
        print(f'Ensuring directory exists at {container_dir}...')
        os.mkdir(container_dir, 0o777)
        print(f'Created directory at {container_dir}')
        with open(f'{container_dir}/{counter_filename}', 'w') as cf:
            print("Opened the counter file..")
            cf.write('0')
            os.mkdir(f'{container_dir}/{storage_dir}', 0o777)
        print(f'Created storage directory at {container_dir}/{storage_dir}')
        
    except FileExistsError as e:
        print(f'Directory {container_dir} already exists.')

def read_counter(simple_container_dir: str, counter_filename: str) -> int:
    container_dir = absolute_path(simple_container_dir)
    with open(f'{container_dir}/{counter_filename}', 'r') as cf:
        cf_text = cf.read()
        cf_num = int(cf_text) if len(cf_text) else 0
        return cf_num
    

def increment_counter(simple_container_dir: str, counter_filename: str):
    container_dir = absolute_path(simple_container_dir)
    cf_num = read_counter(container_dir, counter_filename)
    with open(f'{container_dir}/{counter_filename}', 'w') as cf:
        cf.write(str(cf_num + 1))
