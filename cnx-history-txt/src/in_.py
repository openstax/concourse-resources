import json
import os
import sys

from src.history import build_history_url


def in_(dest_path, in_stream):
    input = json.load(in_stream)

    version = input["version"]["date"]
    instance = input["source"]["instance"]

    version_path = os.path.join(dest_path, "version")
    instance_path = os.path.join(dest_path, "instance.txt")

    with open(version_path, "w") as file:
        file.write(version)

    with open(instance_path, "w") as file:
        file.write(build_history_url(instance))

    return version


def main():
    dest_path = sys.argv[1]
    print(f"Output dir {dest_path}", file=sys.stderr)
    version = in_(dest_path, sys.stdin)
    print(f"Version is {version}", file=sys.stderr)
    print(json.dumps({"version": {"date": version}}))


if __name__ == '__main__':
    main()
