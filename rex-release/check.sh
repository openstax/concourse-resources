#!/bin/bash

SOURCE=`cat`
BUCKET=`echo $SOURCE | jq -r '.source.bucket | select (.!=null)'`
PREFIX=`echo $SOURCE | jq -r '.source.prefix | select (.!=null)'`
VERSION=`echo $SOURCE | jq -r '.version.id | select (.!=null)'`
export AWS_ACCESS_KEY_ID=`echo $SOURCE | jq -r '.source.access_key_id'`
export AWS_SECRET_ACCESS_KEY=`echo $SOURCE | jq -r '.source.secret_access_key'`

RESULTS=`aws s3api list-objects --bucket $BUCKET --prefix rex/releases/$PREFIX`

# only the release.json files, most recent on the top
RESULTS=`echo $RESULTS | jq ".Contents | map(select(.Key | endswith(\"/rex/release.json\"))) | sort_by(.LastModified) | reverse"`

AFTER=""

if [ ! -z "$VERSION" ]
then
  # there is a version, find the timestamp it belongs to
  AFTER=`echo $RESULTS | jq -r ".[] | select(.Key == \"rex/releases/$VERSION/rex/release.json\").LastModified"`
fi

if [ -z "$AFTER" ]
then
  # there is no version, or the version is bad, output the first thing
  RESULTS=`echo $RESULTS | jq "[first]"`
else
  # filter by time
  RESULTS=`echo $RESULTS | jq "map(select(.LastModified >= \"$TARGET\"))"`
fi

echo $RESULTS | jq ".[] | {id: .Key | ltrimstr(\"rex/releases/\") | rtrimstr(\"/rex/release.json\")}"
