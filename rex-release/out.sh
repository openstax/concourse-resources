#!/bin/bash

WORKDIR=$1
if [ -z "$WORKDIR" ]; then
  echo "usage: $0 <path/to/source>"
  exit 1
fi

set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

cd "$WORKDIR"

PAYLOAD=$(mktemp /tmp/resource-in.XXXXXX)

cat > "$PAYLOAD" <&0

DIR=$(jq -r '.params.path | select (.!=null)' < "$PAYLOAD")
BUCKET=$(jq -r '.source.bucket | select (.!=null)' < "$PAYLOAD")
VERSION=$(jq -r '.id | select (.!=null)' < "$DIR"/rex/release.json)
AWS_ACCESS_KEY_ID=$(jq -r '.source.access_key_id' < "$PAYLOAD")
AWS_SECRET_ACCESS_KEY=$(jq -r '.source.secret_access_key' < "$PAYLOAD")
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

aws s3 sync --exclude 'books/*' "$DIR" "s3://$BUCKET/rex/releases/$VERSION"
aws s3 sync --content-type 'text/html' --cache-control 'max-age=0' "$DIR/books/" "s3://$BUCKET/rex/releases/$VERSION/books"

jq -n "{version: {id: \"$VERSION\"}}" >&3
