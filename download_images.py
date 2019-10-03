import os
import sys
import argparse
import pathlib
import glob
import urllib.request
from urllib.parse import urlparse
import shutil

from common import cover_image_pattern, image_pattern

def download_image(url, images_dir_path):
    url_path = pathlib.Path(urlparse(url).path)
    filename = url_path.name
    file_path = images_dir_path / filename

    # Download the file from `url` and save it locally under `filename`:
    with urllib.request.urlopen(url) as r, open(file_path, 'wb') as f:
        shutil.copyfileobj(r, f)


def get_cover_image_url(str):
    result = cover_image_pattern.match(str)
    return result.group('url') if result else None


def get_markdown_image_urls(str):
    urls = [r.groupdict()['url'] for r in image_pattern.finditer(str)]
    return urls


def process_article(article_path):
    print(f'processing {article_path.name}...')
    image_urls = []
    with article_path.open("r", encoding="utf8") as f:
        for line in f:
            cover_image_url = get_cover_image_url(line)
            if cover_image_url:
                image_urls.append(cover_image_url)

            markdown_image_urls = get_markdown_image_urls(line)
            for image_url in markdown_image_urls:
                image_urls.append(image_url)

    if image_urls:
        images_dir_path = article_path.parents[0] / article_path.stem
        os.makedirs(images_dir_path)
        for image_url in image_urls:
            download_image(image_url, images_dir_path)

def get_article_paths(dirname, article_name):
    if article_name:
        return pathlib.Path(dirname).glob(f"*{article}*.md")

    return pathlib.Path(dirname).glob('*.md')


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="markdown files directory")
    parser.add_argument("--article", help="download images for single article")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_args()
    dirname = args.dir
    article = args.article

    article_paths = get_article_paths(dirname, article)

    for article_path in article_paths:
        process_article(article_path)
