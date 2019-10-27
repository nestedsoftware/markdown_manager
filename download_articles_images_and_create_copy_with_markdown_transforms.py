import os
import argparse
import pathlib

from download_devto_articles import download_and_save_articles
from download_images import download_images
from create_copy_with_markdown_transforms import copy_and_transform


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="whose articles to download")
    parser.add_argument("download_dir", help="output files directory")
    parser.add_argument("localized_dir", help="output files directory")
    parser.add_argument("root", nargs="?", default=os.getcwd(),
                        help="starting path")
    parser.add_argument("--article", help="article to download")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    root_path = pathlib.Path(args.root)
    src_dir_path = pathlib.Path(args.download_dir)
    dest_dir_path = pathlib.Path(args.localized_dir)

    download_and_save_articles(args.username, args.download_dir, args.root,
                               args.article)
    download_images(args.root, args.download_dir, args.article)
    copy_and_transform(root_path, src_dir_path, dest_dir_path, args.article,
                       args.username)
