#!/bin/bash

outdir=$1
if [ -z "$outdir" ]; then
  echo "usage: $0 <path/to/dest>"
  exit 1
fi

set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

payload=$(mktemp /tmp/resource-in.XXXXXX)

cat > "$payload" <&0

bucket=$(jq -r '.source.bucket | select (.!=null)' < "$payload")
aws_access_key_id=$(jq -r '.source.access_key_id' < "$payload")
aws_secret_access_key=$(jq -r '.source.secret_access_key' < "$payload")
export AWS_ACCESS_KEY_ID=$aws_access_key_id
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

version=$(jq -r '.version.id | select (.!=null)' < "$payload")
aws s3 cp "s3://$bucket/rex/releases/$version/rex/release.json" "$outdir/rex/release.json"
jq -n "{version: {id: \"$version\"}}" >&3
