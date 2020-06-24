#!/usr/bin/env python3

import requests
import json
import sys
import os

def _in(instream):
    payload = json.load(instream)
    source = payload['source']
    token = source['token']
    repository = source['repository']
    number = list(lastUpdatedIssue.keys())[0]
    date = lastUpdatedIssue[number]
    endpoint = "https://api.github.com/repos/" + repository + "/issues/" + str(number)
    headers = {'Authorization': 'token ' + token}
    connection = requests.get(endpoint, headers=headers)

    if date == connection.json()['updated_at']:
        if not os.path.exists(str(number)):
            os.makedirs(str(number))
    
        with open(str(number) + '/issue.json', 'w+') as issue:
            json.dump(connection.text, issue)
            issue.close()

        title = open(str(number) + '/title.txt', 'w+')
        title.write(connection.json()['title'])
        title.read()
        title.close()

        numfile = open(str(number) + '/number.txt', 'w+')
        numfile.write(str(connection.json()['number']))
        numfile.read()
        numfile.close()

        body = open(str(number) + '/body.txt', 'w+')
        body.write(connection.json()['body'])
        body.read()
        body.close()

    else:
        print("Dates do not match", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print(json.dumps(_in(sys.stdin)))
