import re

JEKYLL_POSTS_DIR = "_posts"
JEKYLL_IMAGES_DIR = "assets/images"

cover_image_regex = r'cover_image:\s*(?P<url>[^\s]+)'
cover_image_pattern = re.compile(cover_image_regex)

alt = r'!\[(?P<alttext>[^\]]*)\]'
url = r'\(\s*(?P<url>[^\s]+)\s*'
title = r'(\"(?P<titletext>[^\"]*)\")?\)'
image_regex = alt + url + title
image_pattern = re.compile(image_regex)


def get_article_paths(dirpath, article_name):
    articles_path = dirpath / JEKYLL_POSTS_DIR

    if article_name:
        return articles_path.glob(f"*{article}*.md")

    return articles_path.glob('*.md')
