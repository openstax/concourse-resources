#!/bin/bash
set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

PAYLOAD=$(mktemp /tmp/resource-in.XXXXXX)

cat > $PAYLOAD <&0

BUCKET=$(jq -r '.source.bucket | select (.!=null)' < $PAYLOAD)
PREFIX=$(jq -r '.source.prefix | select (.!=null)' < $PAYLOAD)
VERSION=$(jq -r '.version.id | select (.!=null)' < $PAYLOAD)
export AWS_ACCESS_KEY_ID=$(jq -r '.source.access_key_id' < $PAYLOAD)
export AWS_SECRET_ACCESS_KEY=$(jq -r '.source.secret_access_key' < $PAYLOAD)

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
  RESULTS=`echo $RESULTS | jq "map(select(.LastModified >= \"$AFTER\"))"`
fi

echo $RESULTS | jq "map({id: .Key | ltrimstr(\"rex/releases/\") | rtrimstr(\"/rex/release.json\")})" >&3
