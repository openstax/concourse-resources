import json
import os
import sys

import requests
from src.history import get_instance_urls


def in_(dest_path, in_stream):
    input = json.load(in_stream)

    date = input["version"]["date"]
    instance = input["source"]["instance"]
    webview_url = get_instance_urls(instance)["webview_url"]

    response = requests.get(f"{webview_url}/version.txt")
    app_versions = response.json()

    with open(os.path.join(dest_path, "version"), "w") as file:
        file.write(date)

    with open(os.path.join(dest_path, "urls.json"), "w") as file:
        json.dump(get_instance_urls(instance), file)

    with open(os.path.join(dest_path, "app_versions.json"), "w") as file:
        json.dump(app_versions, file)

    return {"version": {"date": date}}


def main():
    dest_path = sys.argv[1]
    print(f"Output dir {dest_path}", file=sys.stderr)
    version = in_(dest_path, sys.stdin)
    print(json.dumps(version))


if __name__ == '__main__':
    main()
