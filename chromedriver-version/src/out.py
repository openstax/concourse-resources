import json
import sys

from src.utils import msg


def out(src_path, stdin):
    raise NotImplementedError


def main():
    src_path = sys.argv[1]
    msg("Source dir {}", src_path)
    print(json.dumps(out(src_path, sys.stdin)))
