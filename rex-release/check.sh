#!/bin/bash
set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

payload=$(mktemp /tmp/resource-in.xxxxxx)

cat > "$payload" <&0

bucket=$(jq -r '.source.bucket | select (.!=null)' < "$payload")
prefix=$(jq -r '.source.prefix | select (.!=null)' < "$payload")
mode=$(jq -r '.source.mode | select (.!=null)' < "$payload")
version=$(jq -r '.version.id | select (.!=null)' < "$payload")
aws_access_key_id=$(jq -r '.source.access_key_id' < "$payload")
aws_secret_access_key=$(jq -r '.source.secret_access_key' < "$payload")
export AWS_ACCESS_KEY_ID=$aws_access_key_id
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

if [ "$mode" = "multiple" ]; then
  echo "check is not supported on multiple release resource"
  exit 1;
fi;

results=$(aws s3api list-objects --bucket "$bucket" --prefix "rex/releases/$prefix")

# only the release.json files, most recent on the top
results=$(echo "$results" | jq ".Contents | map(select(.Key | endswith(\"/rex/release.json\"))) | sort_by(.LastModified) | reverse")

after=""

if [ -n "$version" ]
then
  # there is a version, find the timestamp it belongs to
  after=$(echo "$results" | jq -r ".[] | select(.Key == \"rex/releases/$version/rex/release.json\").LastModified")
fi

if [ -z "$after" ]
then
  # there is no version, or the version is bad, output the first thing
  results=$(echo "$results" | jq "[first]")
else
  # filter by time
  results=$(echo "$results" | jq "map(select(.LastModified >= \"$after\"))")
fi

echo "$results" | jq "map({id: .Key | ltrimstr(\"rex/releases/\") | rtrimstr(\"/rex/release.json\")})" >&3
