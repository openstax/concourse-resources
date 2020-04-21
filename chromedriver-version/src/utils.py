import json
import sys

import requests


def msg(msg, *args, **kwargs):
    if args or kwargs:
        msg = msg.format(*args, **kwargs)
    print(msg, file=sys.stderr)


def write_file(filepath, data):
    if filepath.endswith(".json"):
        with open(filepath, "w") as file:
            json.dump(data, file)
    else:
        with open(filepath, "w") as file:
            file.write(data)


def get_chromedriver_version():
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    r = requests.get(url)

    r.raise_for_status()

    return r.text
