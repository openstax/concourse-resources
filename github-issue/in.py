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

    issue = open('./issue.json', 'w+')
    issue.write(issue)
    issue.read()
    issue.close()

    title = open('./title.txt', 'w+')
    title.write(source['title'])
    title.read()
    title.close()

    description = open('./description.txt', 'w+')
    description.write(source['description'])
    description.read()
    description.close()

    number = open('./number.txt', 'w+')
    number.write(source['number'])
    number.read()
    number.close()

    body = open('./body.txt', 'w+')
    body.write(source['body'])
    body.read()
    body.close()

if __name__ == "__main__":
    print(json.dumps(_in(sys.stdin)))
