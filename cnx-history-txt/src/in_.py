import json
import os
import sys

from src.history import get_instance_urls


def in_(dest_path, in_stream):
    input = json.load(in_stream)

    version = input["version"]["date"]
    instance = input["source"]["instance"]

    version_path = os.path.join(dest_path, "version")
    urls_path = os.path.join(dest_path, "urls.json")

    with open(version_path, "w") as file:
        file.write(version)

    with open(urls_path, "w") as file:
        json.dump(get_instance_urls(instance), file)

    return version


def main():
    dest_path = sys.argv[1]
    print(f"Output dir {dest_path}", file=sys.stderr)
    version = in_(dest_path, sys.stdin)
    print(f"Version is {version}", file=sys.stderr)
    print(json.dumps({"version": {"date": version}}))


if __name__ == '__main__':
    main()
