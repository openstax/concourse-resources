#!/bin/bash
set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

payload=$(mktemp /tmp/resource-in.XXXXXX)

cat > "$payload" <&0

url=$(jq -r '.source.url | select (.!=null)' < "$payload")
fn=$(jq -r '.source.fn | select (.!=null)' < "$payload")

curl -sL "$url" | jq "$fn" | jq -c '[{id: .}]' >&3
