#!/usr/bin/env python3

import requests
import json
import sys
import os
import datetime
from pprint import pprint
import dateutil.parser

def _check(instream):
    #payload = json.load(instream)
    source = payload['source']
    token = source['token']
    repository = source['repository']
now = datetime.datetime.now() - datetime.timedelta(seconds = 180)
    date = now.isoformat()

    try:
        issueNumbers
    except NameError:
        issueNumbers = {}

    headers = {'Authorization': 'token ' + token}
    endpoint = "https://api.github.com/repos/" + repository + "/issues"
    connection = requests.get(endpoint, headers=headers)
    
    if issueNumbers = {}:
        for i in connection.json():
            issueNumbers.update( {i['number'] : i['updated_at']})

    for i in connection.json():
        if i['updated_at'] > date:
            issueNumbers.update( {i['number'] : i['updated_at']})

    return issueNumbers


if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))    
