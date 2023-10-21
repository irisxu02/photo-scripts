import os
import shutil
import subprocess
from datetime import datetime
import argparse


# separate photos/video files by time
def separate_photos_by_time(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file):
                creation_time = os.path.getmtime(file_path)
                time_object = datetime.fromtimestamp(creation_time)
                dest = os.path.join(
                    root_dir, f"{time_object.year:04d}-{time_object.month:02d}"
                )
                if not os.path.exists(dest):
                    os.makedirs(dest)
                shutil.move(file_path, os.path.join(dest, file))


# separate photos by type (non-images are put into folder called 'video')
def separate_photos_by_type(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file):
                extension = file.split(".")[-1].lower()
                dest = os.path.join(root_dir, extension)
            else:  # video
                dest = os.path.join(root_dir, "video")

            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.move(file_path, os.path.join(dest, file))


# convert HEIC to JPG
def convert_heic_to_jpg(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(".heic"):
                output_file_path = os.path.splitext(file_path)[0] + ".jpg"
                subprocess.run(["heif-convert", file_path, output_file_path])
                os.remove(file_path)


# check if the file is an image file
def is_image(filename):
    return any(
        filename.lower().endswith(extension)
        for extension in [".arw", ".jpg", ".jpeg", ".png", ".heic"]
    )


# extract all content from subdirectories into the root directory
# assumes that all files have different names
def extract_subdirectories(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            shutil.move(file_path, root_dir, file)
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if directory != root_dir:
                shutil.rmtree(os.path.join(root, directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Photo management automation script.")
    parser.add_argument("--time", action="store_true", help="Separate photos by time")
    parser.add_argument("--type", action="store_true", help="Separate photos by type")
    parser.add_argument("--convert", action="store_true", help="Convert HEIC to JPG")
    parser.add_argument(
        "--extract", action="store_true", help="Extract all content from subdirectories"
    )
    parser.add_argument("directory", help="Directory path")

    args = parser.parse_args()

    if os.path.isdir(args.directory):
        if args.extract:
            extract_subdirectories(args.directory)
            print("Extracted content from subdirectories.")
        if args.convert:
            convert_heic_to_jpg(args.directory)
            print("Converted HEIC to JPG.")
        if args.time:
            separate_photos_by_time(args.directory)
            print("Separated by time (yyyy-mm).")
        if args.type:
            separate_photos_by_type(args.directory)
            print("Separated by file type.")
        print("All done!")
    else:
        print("Invalid directory path.")
