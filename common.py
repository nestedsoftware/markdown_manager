import re
import logging

JEKYLL_POSTS_DIR = "_posts"
JEKYLL_IMAGES_DIR = "assets/images"

ARTICLES_DICT_FILE = "articles_dict.json"

cover_image_regex = r'^cover_image:\s*(?P<url>\S+)'
cover_image_pattern = re.compile(cover_image_regex)

alt = r'!\[(?P<alttext>[^\]]*)\]'
url = r'\(\s*(?P<url>\S+)\s*'
title = r'(?:\"(?P<titletext>[^\"]*)\")?\)'
image_regex = alt + url + title
image_pattern = re.compile(image_regex)

def set_logging_level():
    logging.getLogger().setLevel(logging.INFO)


def get_root_path(dirpath, subdir_name):
    return dirpath / subdir_name


def get_articles_root_path(dirpath):
    return get_root_path(dirpath, JEKYLL_POSTS_DIR)


def get_images_root_path(dirpath):
    return get_root_path(dirpath, JEKYLL_IMAGES_DIR)


def get_article_paths(articles_path, article_name):
    if article_name:
        return articles_path.glob(f"*{article_name}*.md")

    return articles_path.glob('*.md')


def get_relative_article_path(article_filename):
    return (f"{JEKYLL_POSTS_DIR}/{article_filename}" if JEKYLL_POSTS_DIR
            else article_filename)


def get_relative_image_dirname(image_dirname):
    return (f"/{JEKYLL_IMAGES_DIR}/{image_dirname}" if JEKYLL_IMAGES_DIR
            else f"/{image_dirname}")


def replace_colon(a_string):
    return a_string.replace(":", "&#58;")
