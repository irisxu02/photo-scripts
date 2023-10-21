import os

def create_files(root_dir, num_files, count):
    for i in range(count, count + num_files + 1):
        file_name = f"{i}.txt"
        with open(os.path.join(root_dir, file_name), 'w') as f:
            f.write(f"This is file {i}")


def create_directories(root_dir, num_dirs, num_files):
    count = 1
    for i in range(1, num_dirs + 1):
        dir_name = f"directory_{i}"
        dir_path = os.path.join(root_dir, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        create_files(dir_path, num_files, count)
        count = count + num_files + 1
        

if __name__ == "__main__":
    root_directory = "main_directory"
    n_dir = 5
    n_files = 20
    

    if not os.path.exists(root_directory):
        os.makedirs(root_directory)

    create_directories(root_directory, n_dir, n_files)
    print(f"Created {n_dir} directories with {n_files} files each.")

