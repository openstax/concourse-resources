#!/usr/bin/env python3

import requests
import json
import sys
import os
import datetime

def _in(instream):
    payload = json.load(instream)
    source = payload['source']
    token = source['token']
    repository = source['repository']

    version = payload['version']
    versionNumber = list(version.keys())[0]
    versionDate = version[versionNumber]
    print(versionNumber, file=sys.stderr)
    print(versionDate, file=sys.stderr)

    endpoint = "https://api.github.com/repos/" + repository + "/issues/" + versionNumber
    headers = {'Authorization': 'token ' + token}
    connection = requests.get(endpoint, headers=headers)
    now = datetime.datetime.now() - datetime.timedelta(seconds = 180)
    date = now.isoformat()
    print(date, file=sys.stderr)

    if  versionDate >= date:
        with open('issue.json', 'w+') as issue:
            json.dump(connection.text, issue)
            issue.close()

        title = open('title.txt', 'w+')
        title.write(connection.json()['title'])
        title.read()
        title.close()

        numfile = open('number.txt', 'w+')
        numfile.write(str(connection.json()['number']))
        numfile.read()
        numfile.close()

        body = open('body.txt', 'w+')
        body.write(connection.json()['body'])
        body.read()
        body.close()

    else:
        print("Dates do not match", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print(json.dumps(_in(sys.stdin)))
