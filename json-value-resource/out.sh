#!/bin/bash

workdir=$1
if [ -z "$workdir" ]; then
  echo "usage: $0 <path/to/source>"
  exit 1
fi

set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

cd "$workdir"

payload=$(mktemp /tmp/resource-in.XXXXXX)

cat > "$payload" <&0

file=$(jq -r '.params.file | select (.!=null)' < "$payload")
version=$(< "$file")

jq -n "{version: {id: \"$version\"}}" >&3
