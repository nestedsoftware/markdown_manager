import os
import re
import argparse
import pathlib
import shutil
from urllib.parse import urlparse

from common import cover_image_pattern, image_pattern

def copy_image_folders(src_dir_path, dest_dir_path, article_name):
     folders = filter(os.path.isdir, os.scandir(src_dir_path))
     for folder in folders:
        if not article_name or article_name in folder.name:
            shutil.copytree(folder, dest_dir_path / folder.name)

def write_md_files_with_local_path_for_images(src_dir_path, dest_dir_path,
                                              article_name):
    infile_paths = get_article_paths(src_dir_path, article_name)
    for infile_path in infile_paths:
        outfile_path = dest_dir_path / infile_path.name
        with infile_path.open("r", encoding="utf8") as infile, \
             outfile_path.open("a", encoding="utf8") as outfile:
            for line in infile:
                outline = transform_line(infile_path.stem, line)
                outfile.write(outline)


def get_article_paths(dirpath, article_name):
    if article_name:
        return dirpath.glob(f"*{article}*.md")

    return dirpath.glob('*.md')


def get_replace_function(dirname):
    def replace(match):
        matching_string = match.group(0)
        url = match.group('url')
        url_path = pathlib.Path(urlparse(url).path)
        filename = f"{dirname}/{url_path.name}"
        return matching_string.replace(url, f"{filename}")

    return replace


def transform_line(dirname, line):
    replace = get_replace_function(dirname)
    line = re.sub(cover_image_pattern, replace, line)
    return re.sub(image_pattern, replace, line)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("srcdir", help="whose articles to download")
    parser.add_argument("destdir", help="output files directory")
    parser.add_argument("--article", help="download images for single article")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    src_dir_path = pathlib.Path(args.srcdir)
    dest_dir_path = pathlib.Path(args.destdir)
    article = args.article

    copy_image_folders(src_dir_path, dest_dir_path, article)

    write_md_files_with_local_path_for_images(src_dir_path, dest_dir_path,
                                              article)
