#!/usr/bin/env python3

import requests
import json
import sys
import os
import datetime
from pprint import pprint
import dateutil.parser

def _check(instream):
    payload = json.load(instream)
    source = payload['source']
    token = source['token']
    repository = source['repository']
    
    if 'version' in payload:
        since = '&since=' + payload['version']['modified']
    else:
        since = ''

    headers = {'Authorization': 'token ' + token}
    endpoint = "https://api.github.com/repos/" + repository + "/issues?sort=updated&direction=desc" + since
    connection = requests.get(endpoint, headers=headers)

    issues = connection.json()
    issues.reverse()

    results = []
    
    if 'version' in payload:
        for i in issues:
            results.append({"number": str(i['number']), "modified": i['updated_at']})
    else:
        latest = issues[-1]
        if latest:
            results.append({"number": str(latest['number']), "modified": latest['updated_at']})

    return results

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))
