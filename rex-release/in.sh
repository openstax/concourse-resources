#!/bin/bash
set -e

OUTDIR=$1
SOURCE=$(cat)
BUCKET=$(echo $SOURCE | jq -r '.source.bucket | select (.!=null)')
PREFIX=$(echo $SOURCE | jq -r '.source.prefix | select (.!=null)')
VERSION=$(echo $SOURCE | jq -r '.version.id | select (.!=null)')
export AWS_ACCESS_KEY_ID=`echo $SOURCE | jq -r '.source.access_key_id'`
export AWS_SECRET_ACCESS_KEY=`echo $SOURCE | jq -r '.source.secret_access_key'`

aws s3 cp --quiet s3://$BUCKET/rex/releases/$VERSION/rex/release.json $OUTDIR/rex/release.json

jq -n "{version: {id: \"$VERSION\"}}"
