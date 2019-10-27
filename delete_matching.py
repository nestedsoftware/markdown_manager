import os
import argparse
import pathlib
import shutil
import json

from common import ARTICLES_DICT_FILE
from database import ArticlesDatabase

def remove_matches(name, root):
    global articles_db

    root_path = pathlib.Path(root)
    matches = root_path.glob(f"**/*{name}*")
    for match in matches:
        if match.is_dir():
            shutil.rmtree(match)
        else:
            os.remove(match)

    articles_db_path = root_path / ARTICLES_DICT_FILE
    articles_db = ArticlesDatabase(articles_db_path)
    articles_db.delete_record(name)
    articles_db.write_to_file()


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="delete all matching files/dirs")
    parser.add_argument("root", nargs="?", default=os.getcwd(),
                        help="starting path")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    remove_matches(args.name, args.root)
