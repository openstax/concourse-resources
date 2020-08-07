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

version=$(jq -r '.version.id | select (.!=null)' < "$payload")

echo -n "$version" > "$outdir/version.txt"

jq -n "{version: {id: \"$version\"}}" >&3
