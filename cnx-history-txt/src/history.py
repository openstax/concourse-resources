import json

import dateutil.parser

import requests

SUPPORTED_INSTANCES = ['dev', 'qa', 'staging', 'prod']
PROD_URL = "https://cnx.org/history.txt"
HISTORY_URL_TEMPLATE = "https://{0}.cnx.org/history.txt"
RELEASE_DELIMITER = "==============================="
VERSIONS_DELIMITER = "-------------------------------"


def build_history_url(instance):
    if instance == "prod":
        return PROD_URL
    else:
        return HISTORY_URL_TEMPLATE.format(instance)


def get_history_txt(instance):
    url = build_history_url(instance)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_dates_from_releases(history_txt):
    """Extract the dates from the history.txt"""
    # Let's split the releases
    releases = history_txt.replace("\n", "").split(RELEASE_DELIMITER)

    # Last item is a blank line so we remove it.
    del releases[-1]

    release_dates = [json.loads(release.split(VERSIONS_DELIMITER)[0])["date"]
                     for release in releases]

    # Turn release date strings into datetime objects
    release_dates = [dateutil.parser.parse(t) for t in release_dates]

    return release_dates


def get_release_dates(instance):
    releases_text = get_history_txt(instance)
    release_dates = parse_dates_from_releases(releases_text)
    release_dates.sort()
    return release_dates


def get_newest_dates(lst, value):
    for index, val in enumerate(lst):
        if val >= value:
            return lst[index:]
    return [lst[-1]]
