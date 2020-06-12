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
    endpoint = "https://api.github.com/repos/" + repository + "/issues/" + number
    headers = {'Authorization': 'token ' + token}

    connection = requests.get(endpoint, headers=headers)
    i = json.loads(connection.text)

    for item in issueNumbers:
        number = item
        endpoint = "https://api.github.com/repos/" + repository + "/issues/" + number
        connection = requests.get(endpoint, headers=headers)
        i = json.loads(connection.text)
        if issueNumber[item] == i['updated_at']:
            if not os.path.exists(str(number)):
                os.makedirs(str(number))
        
            issue = open(str(number) + '/issue.json', 'w+')
            json.loads(connection.text, issue)
            issue.close()

            title = open(str(number) + '/title.txt', 'w+')
            title.write(item['title'])
            title.read()
            title.close()
    
            number = open(str(number) + '/number.txt', 'w+')
            number.write(str(item['number']))
            number.read()
            number.close()

            body = open(str(number) + '/body.txt', 'w+')
            body.write(item['body'])
            body.read()
            body.close()

if __name__ == "__main__":
    print(json.dumps(_in(sys.stdin)))
