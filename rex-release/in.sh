#!/bin/bash

OUTDIR=$1
if [ -z "$OUTDIR" ]; then
  echo "usage: $0 <path/to/dest>"
  exit 1
fi

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

aws s3 cp s3://$BUCKET/rex/releases/$VERSION/rex/release.json $OUTDIR/rex/release.json

jq -n "{version: {id: \"$VERSION\"}}" >&3
