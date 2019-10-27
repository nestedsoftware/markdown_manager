import os
import argparse
import pathlib
import shutil
import json

from common import ARTICLES_DICT_FILE


def remove_matches(name, root):
    path = pathlib.Path(root)
    matches = path.glob(f"**/*{name}*")
    for match in matches:
        if match.is_dir():
            shutil.rmtree(match)
        else:
            os.remove(match)

    remove_from_articles_dict(path, name)


def remove_from_articles_dict(path, name):
    articles_dict_path = path / ARTICLES_DICT_FILE
    articles_dict = None
    with open(articles_dict_path, 'r', encoding='utf-8') as f:
        articles_dict = json.load(f)

    found_key = find_key(articles_dict, name)
    if found_key:
        value = articles_dict.pop(found_key)
        os.remove(articles_dict_path)
        with open(articles_dict_path, 'w', encoding='utf-8') as f:
            json.dump(articles_dict, f, ensure_ascii=False, indent=4)


def find_key(articles_dict, name):
    found_key = None
    for key in articles_dict:
        if name in key:
            found_key = key
    return found_key


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="delete all matching files/dirs")
    parser.add_argument("root", nargs="?", default=os.getcwd(),
                        help="starting path")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    remove_matches(args.name, args.root)
