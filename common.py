import re

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


def get_root_path(dirpath, subdir_name):
    return dirpath / subdir_name


def get_articles_root_path(dirpath):
    return get_root_path(dirpath, JEKYLL_POSTS_DIR)


def get_images_root_path(dirpath):
    return get_root_path(dirpath, JEKYLL_IMAGES_DIR)


def get_article_paths(dirpath, article_name):
    articles_path = get_root_path(dirpath, JEKYLL_POSTS_DIR)

    if article_name:
        return articles_path.glob(f"*{article}*.md")

    return articles_path.glob('*.md')

def replace_colon(a_string):
    return a_string.replace(":", "&#58;")
