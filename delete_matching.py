import os
import argparse
import pathlib
import shutil


def remove_matches(name, root):
    path = pathlib.Path(root)
    matches = path.glob(f"**/*{name}*")
    for match in matches:
        if match.is_dir():
            shutil.rmtree(match)
        else:
            os.remove(match)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="delete all matching files/dirs")
    parser.add_argument("root", nargs="?", default=os.getcwd(),
                        help="starting path")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    remove_matches(args.name, args.root)
