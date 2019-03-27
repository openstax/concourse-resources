import json
import sys

import dateutil.parser

from src.history import get_newest_dates, get_release_dates


def check(in_stream):
    input = json.load(in_stream)
    instance = input["source"]["instance"]
    release_dates = get_release_dates(instance)

    if input["version"]:
        previous_date = dateutil.parser.parse(input['version']['date'])
        release_dates = get_newest_dates(release_dates, previous_date)

    release_dates = [{"date": date.strftime("%Y-%m-%d %-H:%M:%S %Z")} for date in release_dates]

    return release_dates


def main():
    print(json.dumps(check(sys.stdin)))


if __name__ == '__main__':
    main()
