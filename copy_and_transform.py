import errno
import os
import json
import re
import argparse
import pathlib
import shutil
from urllib.parse import urlparse

from common import cover_image_pattern, image_pattern
from common import ARTICLES_DICT_FILE
from common import (get_articles_root_path, get_images_root_path,
                    get_article_paths, get_relative_article_path,
                    get_relative_image_dirname, replace_colon)

from database import ArticlesDatabase

link_regex = r'''
    {%\s*link\s*
    (?P<url>(?:https?://dev.to)?
    /?(?P<username>\S+?)/
    (?P<filename>\S+))/?\s*%}'''
link_pattern = re.compile(link_regex, re.VERBOSE)

md_link_regex = r'''
    \[.*\]\((?:\s*)
    (?P<url>(?:https?://dev\.to)?
    /(?P<username>[^/\\]+)/
    (?P<filename>[^\)\s]+)).*\)'''
md_link_pattern = re.compile(md_link_regex, re.VERBOSE)

title_regex = r'^title:\s*(?P<title>\S+(?:\s+\S+)*)'
title_pattern = re.compile(title_regex)

gist_regex = r'{%\s*gist\s*(?P<url>\S+\/(?P<gistid>[^\/\s]+))\/?\s*%}'
gist_pattern = re.compile(gist_regex)

github_regex = r'{%\s*github\s*(?P<url>\S+)\s*%}'
github_pattern = re.compile(github_regex)

heading_regex = r'(?:^\s*|^)(?:#+)(?:\b)'
heading_pattern = re.compile(heading_regex)

filename_regex = r'^(?P<date>\d{4}-\d{2}-\d{2})-(?P<main>[^.]+)'
filename_pattern = re.compile(filename_regex)


def copy_and_transform(root_path, src_dir_path, dest_dir_path, username,
                       article_name):
    copy_image_folders(root_path, src_dir_path, dest_dir_path, article_name)
    transform_markdown_files(root_path, src_dir_path, dest_dir_path,
                             article_name, username)


def copy_image_folders(root_path, src_dir_path, dest_dir_path, article_name):
    images_root_path = get_images_root_path(root_path / src_dir_path)
    images_root_dest_path = get_images_root_path(root_path / dest_dir_path)

    if not article_name:
        with os.scandir(images_root_path) as folders:
            for folder in folders:
                if os.path.isdir(folder):
                    destination_folder = images_root_dest_path / folder.name
                    shutil.copytree(folder, destination_folder)
    else:
        article_root_path = get_articles_root_path(root_path / src_dir_path)
        article_paths = get_article_paths(article_root_path, article_name)
        article_paths_list = list(article_paths)
        assert len(article_paths_list) == 1, "should only be one match"
        article_path = article_paths_list[0]

        images_dir_file_path = images_root_path / article_path.stem
        images_dir_dest_file_path = images_root_dest_path / article_path.stem

        shutil.copytree(images_dir_file_path, images_dir_dest_file_path)


def transform_markdown_files(root_path, src_dir_path, dest_dir_path,
                             article_name, username):
    articles_root_path = get_articles_root_path(root_path / src_dir_path)
    articles_root_dest_path = get_articles_root_path(root_path / dest_dir_path)

    articles_db_path = root_path / ARTICLES_DICT_FILE
    articles_db = ArticlesDatabase(articles_db_path)

    if not article_name:
        os.makedirs(articles_root_dest_path, exist_ok=True)

    infile_paths = get_article_paths(articles_root_path, article_name)
    for infile_path in infile_paths:
        outfile_path = articles_root_dest_path / infile_path.name
        with infile_path.open("r", encoding="utf8") as infile, \
             outfile_path.open("a", encoding="utf8") as outfile:
            for line in infile:
                image_dirname = get_relative_image_dirname(outfile_path.stem)
                outline = transform_line(articles_db, line, username,
                                         root_path, src_dir_path,
                                         dest_dir_path, image_dirname)
                outfile.write(outline)


def transform_line(articles_db, line, username, root_path, src_dir_path,
                   dest_dir_path, image_dirname):
    replace = get_localize_image(image_dirname)
    line = re.sub(cover_image_pattern, replace, line)
    line = re.sub(image_pattern, replace, line)

    replace = get_transform_liquid_link_tag(articles_db, username,
                                            root_path, src_dir_path)
    line = re.sub(link_pattern, replace, line)

    replace = get_transform_markdown_link_tag(username, root_path,
                                              src_dir_path)
    line = re.sub(md_link_pattern, replace, line)

    replace = get_transform_colon_in_title()
    line = re.sub(title_pattern, replace, line)

    replace = get_transform_liquid_gist_tag()
    line = re.sub(gist_pattern, replace, line)

    replace = get_transform_liquid_github_tag()
    line = re.sub(github_pattern, replace, line)

    replace = get_transform_heading()
    line = re.sub(heading_pattern, replace, line)

    return line


def get_localize_image(dirname):
    def replace(match):
        matching_string = match.group(0)
        url = match.group('url')
        url_path = pathlib.Path(urlparse(url).path)
        filename = f"{dirname}/{url_path.name}"

        replacement = matching_string

        try:
            alttext = match.group('alttext')
            replacement_alttext = alttext.replace('*', '&#42;')
            replacement = replacement.replace(alttext, replacement_alttext)
        except IndexError:
            pass

        replacement = replacement.replace(url, filename)
        return replacement

    return replace


def get_transform_liquid_link_tag(articles_db, username, root_path,
                                  src_dir_path):
    def replace(match):
        matching_string = match.group(0)
        link_path = match.group('url')
        filename_part = match.group('filename')
        matched_username = match.group('username')


        if is_self_link(username, matched_username, link_path):
            pathname = get_local_file_path(filename_part, root_path,
                                           src_dir_path)
            replacement = matching_string.replace(link_path, pathname)
            title = articles_db.get_record(pathname)["title"]
            return f"* [{title}]({replacement})"

        pathname = (f"https://dev.to/{link_path}" if is_local_link(link_path)
                    else link_path)
        return f"* [{pathname}]({pathname})"

    return replace


def get_transform_markdown_link_tag(username, root_path, src_dir_path):
    def replace(match):
        matching_string = match.group(0)
        link_path = match.group('url')
        filename_part = match.group('filename')
        matched_username = match.group('username')

        if is_self_link(username, matched_username, link_path):
            pathname = get_local_file_path(filename_part, root_path,
                                           src_dir_path)
            local_link = f"{{% link {pathname} %}}"
            replacement = matching_string.replace(link_path, local_link)
            return replacement

        return matching_string

    return replace


def is_self_link(username, matched_username, url):
    if not is_local_link(url):
        return False

    return matched_username == username and '/comments' not in url


def is_local_link(url):
    if 'http' not in url:
        return True

    return 'dev.to' in url


def get_local_file_path(filename_part, root_path, src_dir_path):
    search_path = root_path / src_dir_path
    found_files = list(search_path.glob(f"**/*{filename_part}*.md"))

    assert len(found_files) > 0, "there should be at least one match"
    if len(found_files) > 1:
        relative_article_path = None
        for file in found_files:
            if is_filename_a_match(filename_part, file.name):
                relative_article_path = get_relative_article_path(file.name)
                if relative_article_path:
                    break;

        if not relative_article_path:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    filename_part)
        return relative_article_path

    filename = found_files[0].name
    return get_relative_article_path(filename)


def is_filename_a_match(filename_part, filename):
    result = filename_pattern.match(filename)
    return_value = result and result.group("main") == filename_part
    return return_value


def get_transform_colon_in_title():
    def replace(match):
        matching_string = match.group(0)
        title = match.group('title')
        updated_title = replace_colon(title)
        return matching_string.replace(title, updated_title)

    return replace


def get_transform_liquid_gist_tag():
    def replace(match):
        matching_string = match.group(0)
        url = match.group('url')
        gistid = match.group('gistid')
        return matching_string.replace(url, gistid)

    return replace


def get_transform_liquid_github_tag():
    def replace(match):
        matching_string = match.group(0)
        url = match.group('url')
        if 'http' not in url:
            url = f"https://github.com/{url}"

        return f"* [{url}]({url})"

    return replace


def get_transform_heading():
    def replace(match):
        matching_string = match.group(0)
        return f"{matching_string} "

    return replace


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=os.getcwd(), help="base path")
    parser.add_argument("--download_dir", default="downloaded_files",
                        help="downloaded files directory")
    parser.add_argument("--transformed_dir", default="transformed_files",
                        help="transformed files directory")
    parser.add_argument("--username", help="owner of this blog")
    parser.add_argument("--article", help="download images for single article")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    root_path = pathlib.Path(args.root)
    download_dir_path = pathlib.Path(args.download_dir)
    transformed_dir_path = pathlib.Path(args.transformed_dir)
    username = args.username
    article = args.article

    copy_and_transform(root_path, download_dir_path, transformed_dir_path,
                       username, article)
