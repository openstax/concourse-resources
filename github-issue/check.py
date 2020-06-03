#!/usr/bin/env python3

import requests
import json
import sys
import os
from pprint import pprint

def msg(msg, *args, **kwargs):
  if isinstance(msg, dict):
    pprint(msg, stream=sys.stderr)
  else:
    print(msg.format(*args, **kwargs), file=sys.stderr)

def get_versions():
    if os.path.exists('versions.json'):
        with open('versions.json', 'r') as f:
          versions = json.load(f)
    else:
        versions = {'versions': []}
        return versions

def update_versions(id, versions):
    versions['versions'] += [id]
    with open('versions.json', 'w') as f:
        json.dump(versions, f)

def _check(instream):
    payload = json.load(instream)
    source = payload['source']
    try:
        versions = get_versions()
    except:
        versions = {'versions': []}
    msg('''CHECK
    Versions {}
    ''', versions)

    token = source['token']
    repository = source['repository']
    number = source['number']

    endpoint = "https://api.github.com/repos/" + repository + "/issues/" + number
    headers = {'Authorization': 'token ' + token}

    connection = requests.get(endpoint, headers=headers)
    issue = json.loads(connection.text)
    ver = issue['updated_at']

    if ver not in versions['versions']:
        update_versions(ver, versions)
        return [{"version" : ver}]

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))    
