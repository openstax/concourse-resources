import json
import sys

from src.utils import get_chromedriver_version


def check(in_stream):
    input = json.load(in_stream)
    version = input.get("version")

    if not version:
        return [{"version": get_chromedriver_version()}]
    else:
        current_version = get_chromedriver_version()
        previous_version = version["version"]
        # We're going to assume that chromedriver
        # is always updated to a newer version.
        if current_version == previous_version:
            return []
        else:
            return [{"version": current_version}]


def main():
    print(json.dumps(check(sys.stdin)))


if __name__ == "__main__":
    main()
