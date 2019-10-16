import os
import json
import re
import argparse
import pathlib
import shutil
from urllib.parse import urlparse

from common import cover_image_pattern, image_pattern
from common import JEKYLL_IMAGES_DIR
from common import (get_articles_root_path, get_images_root_path,
                    get_article_paths, ARTICLES_DICT_FILE)

articles_dict = {}

liquid_link_regex = r'\{%\s*link\s*(?P<url>[^\s]+)\s*%\}'
liquid_link_pattern = re.compile(liquid_link_regex)

title_regex = r'^title:\s*(?P<title>\S+(?:\s+\S+)*)'
title_pattern = re.compile(title_regex)

gist_regex = r'{%\s*gist\s*\S+\/(?P<gistid>[^\/\s]+)\/?\s*%}'
gist_pattern = re.compile(gist_regex)

def get_image_dirname(images_root_path, image_dirname):
    dirname = ""
    parts = images_root_path.parts
    if len(parts) > 1:
        dirname += "/"
        for i in range(1, len(parts)):
            dirname += f"{parts[i]}/"

    dirname += image_dirname

    return dirname


def copy_and_transform(src_dir_path, dest_dir_path, article_name, username):
    global articles_dict
    with open(ARTICLES_DICT_FILE, 'r', encoding='utf-8') as f:
        articles_dict = json.load(f)

    copy_image_folders(src_dir_path, dest_dir_path, article_name)
    transform_markdown_files(src_dir_path, dest_dir_path, article_name,
                             username)


def copy_image_folders(src_dir_path, dest_dir_path, article_name):
    def is_images_dir(entry):
        return os.path.isdir(entry) and (entry.name in JEKYLL_IMAGES_DIR
                                         or not JEKYLL_IMAGES_DIR)

    folders = filter(is_images_dir, os.scandir(src_dir_path))
    for folder in folders:
        if not article_name or article_name in folder.name:
            shutil.copytree(folder, dest_dir_path / folder.name)

def transform_markdown_files(src_dir_path, dest_dir_path, article_name,
                             username):
    images_root_path = get_images_root_path(dest_dir_path)

    output_dir_path = get_articles_root_path(pathlib.Path(dest_dir_path))

    if len(images_root_path.parts) > 1:
        os.makedirs(output_dir_path)

    infile_paths = get_article_paths(src_dir_path, article_name)
    for infile_path in infile_paths:
        outfile_path = output_dir_path / infile_path.name
        with infile_path.open("r", encoding="utf8") as infile, \
             outfile_path.open("a", encoding="utf8") as outfile:
            for line in infile:
                image_dirname = get_image_dirname(images_root_path,
                                                  outfile_path.stem)
                outline = transform_line(image_dirname, line, username,
                                         src_dir_path, dest_dir_path)
                outfile.write(outline)


def transform_line(dirname, line, username, src_dir_path, dest_dir_path):
    replace = get_localize_image_function(dirname)
    line = re.sub(cover_image_pattern, replace, line)
    line = re.sub(image_pattern, replace, line)

    replace = get_transform_liquid_link_tag(username, src_dir_path,
                                            dest_dir_path)
    line = re.sub(liquid_link_pattern, replace, line)

    replace = get_transform_colon_in_title()
    line = re.sub(title_pattern, replace, line)


    # replace = get_transform_liquid_gist_tag()
    # line = re.sub(liquid_gist_tag_pattern, replace, line)

    # replace =get_transform_liquid_github_tag()
    # line = re.sub(liquid_github_tag_pattern, replace, line)

    return line


def get_localize_image_function(dirname):
    def replace(match):
        matching_string = match.group(0)
        url = match.group('url')
        url_path = pathlib.Path(urlparse(url).path)
        filename = f"{dirname}/{url_path.name}"
        replacement = matching_string.replace(url, f"{filename}")
        return replacement

    return replace


def get_transform_liquid_link_tag(username, src_dir_path, dest_dir_path):
    def replace(match):
        matching_string = match.group(0)
        link = match.group('url')

        if username in link:
            filename_part = link.split("/")[-1]
            matches = list(src_dir_path.glob(f"**/*{filename_part}*.md"))
            assert len(matches) == 1, "should only be one match"
            filename = matches[0].name
            root = get_articles_root_path(dest_dir_path)
            pathname = f"{root.name}/{filename}"
            replacement = matching_string.replace(link, pathname)
            title = articles_dict[pathname]["title"]
            return f"[{title}]({replacement})"

        pathname = f"https://dev.to/{link}"
        return pathname

    return replace


def get_transform_colon_in_title():
    def replace(match):
        matching_string = match.group(0)
        title = match.group('title')
        updated_title = title.replace(":", "&#58;")
        return matching_string.replace(title, updated_title)

    return replace


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("srcdir", help="whose articles to download")
    parser.add_argument("destdir", help="output files directory")
    parser.add_argument("--username", help="owner of this blog")
    parser.add_argument("--article", help="download images for single article")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    src_dir_path = pathlib.Path(args.srcdir)
    dest_dir_path = pathlib.Path(args.destdir)
    username = args.username
    article = args.article

    copy_and_transform(src_dir_path, dest_dir_path, article, username)
