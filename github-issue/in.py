#!/usr/bin/env python3

import requests
import json
import sys
import os

def _in(instream):
    payload = json.load(instream)
    source = payload["source"]

    token = source["token"]
    repository = source["repository"]
    number = source["number"]

    endpoint = "https://api.github.com/repos/" + repository + "/issues/" + number
    headers = {'Authorization': 'token ' + token}

    connection = requests.get(endpoint, headers=headers)
    i = json.loads(connection.text)

    issue = open('./issue.json', 'w+')
    json.dump(i, issue)
    issue.close()

    title = open('./title.txt', 'w+')
    title.write(i['title'])
    title.read()
    title.close()

    number = open('./number.txt', 'w+')
    number.write(str(i['number']))
    number.read()
    number.close()

    body = open('./body.txt', 'w+')
    body.write(i['body'])
    body.read()
    body.close()

if __name__ == "__main__":
    print(json.dumps(_in(sys.stdin)))
