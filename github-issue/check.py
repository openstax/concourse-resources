#!/usr/bin/env python3

import requests
import json
import sys
import os
import datetime
from pprint import pprint
import dateutil.parser

def msg(msg, *args, **kwargs):
  if isinstance(msg, dict):
    pprint(msg, stream=sys.stderr)
  else:
    print(msg.format(*args, **kwargs), file=sys.stderr)

def get_newest_dates(lst, value):
    for index, val in enumerate(lst):
        if val >= value:
            return lst[index:]
    return [lst[-1]]

def _check(instream):
    payload = json.load(instream)
    source = payload['source']

    token = source['token']
    repository = source['repository']
    number = source['number']

    endpoint = "https://api.github.com/repos/" + repository + "/issues/" + number
    headers = {'Authorization': 'token ' + token}

    connection = requests.get(endpoint, headers=headers)
    issue = json.loads(connection.text)
    # issue = connection.json

    if source['version']['date'] == "":
        newest_dates = [dateutil.parser.parse(issue['updated_at'])]
    else:
        previous_date = dateutil.parser.parse(source['version']['date'])
        newest_dates = get_newest_dates(newest_dates, previous_date)

    newest_dates = [{"date": date.strftime("%Y-%m-%d %-H:%M:%S %Z")} for date in newest_dates]

    return newest_dates

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))    
