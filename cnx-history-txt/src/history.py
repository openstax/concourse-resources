import json

import dateutil.parser

import requests

HISTORY_URL_TEMPLATE = "{0}/history.txt"
RELEASE_DELIMITER = "==============================="
VERSIONS_DELIMITER = "-------------------------------"
INSTANCE_URLS = {
    "prod": {"legacy_url": "https://legacy.cnx-org",
             "archive_url": "https://archive.cnx.org",
             "webview_url": "https://cnx.org"},
    "dev": {"legacy_url": "https://legacy-dev.cnx-org",
            "archive_url": "https://archive-dev.cnx.org",
            "webview_url": "https://dev.cnx.org"},
    "qa": {"legacy_url": "https://legacy-qa.cnx-org",
           "archive_url": "https://archive-qa.cnx.org",
           "webview_url": "https://qa.cnx.org"},
    "staging": {"legacy_url": "https://legacy-staging.cnx-org",
                "archive_url": "https://archive-staging.cnx.org",
                "webview_url": "https://staging.cnx.org"},
}


def get_instance_urls(instance):
    try:
        urls = INSTANCE_URLS[instance]
    except KeyError:
        raise Exception("You have attempted to use an unsupported instance")

    return urls


def build_history_url(instance):
    return HISTORY_URL_TEMPLATE.format(instance["webview_url"])


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
