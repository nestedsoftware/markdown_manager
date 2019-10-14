import os
import re
import argparse
import pathlib
import shutil
from urllib.parse import urlparse

from common import cover_image_pattern, image_pattern
from common import get_article_paths
from common import JEKYLL_POSTS_DIR, JEKYLL_IMAGES_DIR


def copy_and_localize(src_dir_path, dest_dir_path, article_name):
    copy_image_folders(src_dir_path, dest_dir_path, article_name)
    write_localized_markdown_files(src_dir_path, dest_dir_path, article_name)


def copy_image_folders(src_dir_path, dest_dir_path, article_name):
    def is_images_dir(entry):
        return os.path.isdir(entry) and (entry.name in JEKYLL_IMAGES_DIR
                                         or not JEKYLL_IMAGES_DIR)

    folders = filter(is_images_dir, os.scandir(src_dir_path))
    for folder in folders:
        if not article_name or article_name in folder.name:
            shutil.copytree(folder, dest_dir_path / folder.name)

def write_localized_markdown_files(src_dir_path, dest_dir_path, article_name):
    images_root_path = dest_dir_path / JEKYLL_IMAGES_DIR

    output_dir_path = pathlib.Path(dest_dir_path) / JEKYLL_POSTS_DIR
    os.makedirs(output_dir_path)

    infile_paths = get_article_paths(src_dir_path, article_name)
    for infile_path in infile_paths:
        outfile_path = output_dir_path / infile_path.name
        with infile_path.open("r", encoding="utf8") as infile, \
             outfile_path.open("a", encoding="utf8") as outfile:
            for line in infile:
                image_dirname = f"/{JEKYLL_IMAGES_DIR}/{outfile_path.stem}"
                outline = transform_line(image_dirname, line)
                outfile.write(outline)


def transform_line(dirname, line):
    replace = get_replace_function(dirname)
    line = re.sub(cover_image_pattern, replace, line)
    return re.sub(image_pattern, replace, line)


def get_replace_function(dirname):
    def replace(match):
        matching_string = match.group(0)
        url = match.group('url')
        url_path = pathlib.Path(urlparse(url).path)
        filename = f"{dirname}/{url_path.name}"
        replacement = matching_string.replace(url, f"{filename}")
        return replacement

    return replace


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

    copy_and_localize(src_dir_path, dest_dir_path, article)
