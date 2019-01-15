#!/bin/bash
set -e

pwd
ls

SOURCE=$(cat)
DIR=$(echo $SOURCE | jq -r '.params.path | select (.!=null)')
BUCKET=$(echo $SOURCE | jq -r '.source.bucket | select (.!=null)')
PREFIX=$(echo $SOURCE | jq -r '.source.prefix | select (.!=null)')
VERSION=$(jq -r '.id | select (.!=null)' < $DIR/rex/release.json)
export AWS_ACCESS_KEY_ID=$(echo $SOURCE | jq -r '.source.access_key_id')
export AWS_SECRET_ACCESS_KEY=$(echo $SOURCE | jq -r '.source.secret_access_key')

aws s3 sync --exclude 'books/*' $DIR s3://$BUCKET/rex/releases/$VERSION
aws s3 sync --content-type 'text/html' $DIR/books/ s3://$BUCKET/rex/releases/$VERSION/books

jq -n "{version: {id: \"$VERSION\"}}"
