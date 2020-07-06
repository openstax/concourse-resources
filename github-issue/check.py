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
    try:
        version = [payload['version']]
    except (KeyError,NameError):
        version = []

    headers = {'Authorization': 'token ' + token}

    # first get the last page if it exists
    endpoint = "https://api.github.com/repos/" + repository + "/issues?sort=updated&direction=asc"
    connection = requests.get(endpoint, headers=headers)
    link = connection.headers.get('link')
    if link is not None:
        links = link.split(',')
        for link in links:
            if 'rel="last"' in link:
                endpoint = link[link.find("<")+1:link.find(">")]

    if version is None:
        version = []
    
    if version == []:
        connection = requests.get(endpoint, headers=headers)
        number = connection.json()[-1]['number']
        updated_at = connection.json()[-1]['updated_at']
        version.append( {"number": str(number), "modified": updated_at})
        latest_issue = version
        return latest_issue

    else:
        last_modified = version[-1]['modified']
        dates = {v['modified'] for v in version}
        endpoint = "https://api.github.com/repos/" + repository + "/issues?sort=updated&direction=asc&since=" + last_modified
        connection = requests.get(endpoint, headers=headers)
        for i in connection.json():
            if i['updated_at'] in dates:
                continue
            version.append({"number": str(i['number']), "modified": i['updated_at']})
            dates.add(i['updated_at'])
        issues_updated_since = version
        return issues_updated_since

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))