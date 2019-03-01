import json
import sys


def out(instream):
    pass


def main():
    print(json.dumps(out(sys.stdin)))


if __name__ == '__main__':
    main()
