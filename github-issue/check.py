#!/usr/bin/env python3

import requests
import json
import sys
import os
import datetime
from pprint import pprint
import dateutil.parser
from urllib.parse import urlencode

def _check(instream):
    payload = json.load(instream)
    source = payload['source']
    token = source['token']
    repository = source['repository']
    params = source.get('params', {})

    if 'version' in payload:
        params['since'] = payload['version']['modified']

    params['sort'] = 'updated'
    params['direction'] = 'desc'

    headers = {'Authorization': 'token ' + token}
    endpoint = "https://api.github.com/repos/" + repository + "/issues?" + urlencode(params)
    connection = requests.get(endpoint, headers=headers)

    issues = connection.json()
    issues.reverse()

    results = []

    # if version is not provided only return the most recent entry
    if 'version' not in payload:
        issues = issues[-1:]

    for i in issues:
        results.append({"number": str(i['number']), "modified": i['updated_at']})

    return results

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))
