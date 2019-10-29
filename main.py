import os
import argparse
import pathlib

from download_articles import download_and_save_articles
from download_images import download_images
from copy_and_transform import copy_and_transform


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="whose articles to download")
    parser.add_argument("--root", default=os.getcwd(), help="base path")
    parser.add_argument("--download_dir", default="downloaded_files",
                        help="downloaded files directory")
    parser.add_argument("--transformed_dir", default="transformed_files",
                        help="transformed files directory")
    parser.add_argument("--article", help="article to download")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    root_path = pathlib.Path(args.root)
    download_dir_path = pathlib.Path(args.download_dir)
    transformed_dir_path = pathlib.Path(args.transformed_dir)

    download_and_save_articles(args.username, args.root, args.download_dir,
                               args.article)
    download_images(args.root, args.download_dir, args.article)
    copy_and_transform(root_path, download_dir_path, transformed_dir_path,
                       args.username, args.article)
