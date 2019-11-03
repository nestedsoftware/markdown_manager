import os
import sys
import argparse
import pathlib
import glob
import logging
import shutil

from logging import Logger

import urllib.request
from  urllib.error import HTTPError, URLError
from urllib.parse import urlparse

from common import cover_image_pattern, image_pattern
from common import (JEKYLL_IMAGES_DIR, get_images_root_path, get_article_paths,
                    get_articles_root_path)

logging.getLogger().setLevel(logging.INFO)


def download_images(root, dirname, article_name):
    base_path = pathlib.Path(root) / dirname
    articles_root_path = get_articles_root_path(base_path)
    article_file_paths = get_article_paths(articles_root_path, article_name)
    for article_file_path in article_file_paths:
        process_article(base_path, article_file_path)


def process_article(base_path, article_file_path):
    logging.info(f'downloading images for {article_file_path.name}...')
    image_urls = []
    with article_file_path.open("r", encoding="utf8") as f:
        for line in f:
            cover_image_url = get_cover_image_url(line)
            if cover_image_url:
                image_urls.append(cover_image_url)

            markdown_image_urls = get_markdown_image_urls(line)
            for image_url in markdown_image_urls:
                image_urls.append(image_url)

    if image_urls:
        images_root_path = get_images_root_path(base_path)
        images_dir_path = images_root_path / article_file_path.stem
        os.makedirs(images_dir_path)

        for image_url in image_urls:
            download_image(image_url, images_dir_path)


def get_cover_image_url(str):
    result = cover_image_pattern.match(str)
    return result.group('url') if result else None


def get_markdown_image_urls(str):
    urls = [r.groupdict()['url'] for r in image_pattern.finditer(str)]
    return urls


def download_image(url, images_dir_path):
    url_path = pathlib.Path(urlparse(url).path)
    filename = url_path.name
    image_file_path = images_dir_path / filename

    # Download the file from `url` and save it locally under `filename`:
    try :
        with urllib.request.urlopen(url) as r, open(image_file_path, 'wb') as f:
            shutil.copyfileobj(r, f)
    except (HTTPError, URLError) as e:
        logging.error(f"error downloading image: {url}, {e}")

def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=os.getcwd(), help="base path")
    parser.add_argument("--download_dir", default="downloaded_files",
                        help="downloaded files directory")
    parser.add_argument("--article", help="download images for single article")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_args()
    download_images(args.root, args.download_dir, args.article)