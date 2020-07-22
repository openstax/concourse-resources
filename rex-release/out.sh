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

dir=$(jq -r '.params.path | select (.!=null)' < "$payload")
mode=$(jq -r '.source.mode | select (.!=null)' < "$payload")
bucket=$(jq -r '.source.bucket | select (.!=null)' < "$payload")
aws_access_key_id=$(jq -r '.source.access_key_id' < "$payload")
aws_secret_access_key=$(jq -r '.source.secret_access_key' < "$payload")
export AWS_ACCESS_KEY_ID=$aws_access_key_id
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

upload-release() {
  path=$1
  version=$2

  # everything outside books gets uploaded nicely and can have long cache becaue it is loaded from versioned url
  aws s3 sync --exclude 'books/*' --include 'service-worker.js' --cache-control 'max-age=31536000'  "$path" "s3://$bucket/rex/releases/$version"

  # service worker uploaded separately to have the right content-type, loaded unversioned so no cloudfront caching
  aws s3 sync --exclude '*' --include 'service-worker.js' --cache-control 'max-age=0'  "$path/books/" "s3://$bucket/rex/releases/$version/books"

  # books files with explicit content type set because they don't have extensions, loaded unversioned so no cloudfront caching
  aws s3 sync --exclude 'service-worker.js' --content-type 'text/html' --cache-control 'max-age=0' "$path/books/" "s3://$bucket/rex/releases/$version/books"
}


if [ "$mode" = "multiple" ]; then
  versions_array=()

  for release_dir in "$dir"/*
  do
    version=$(jq -r '.id | select (.!=null)' < "$release_dir"/rex/release.json)
    versions_array+=("$version")
    upload-release "$release_dir" "$version"
  done;

  versions=$(IFS=, ; echo "${versions[*]}")

  jq -n "{version: {ids: \"$versions\"}}" >&3
else
  version=$(jq -r '.id | select (.!=null)' < "$dir"/rex/release.json)
  upload-release "$dir" "$version"
  jq -n "{version: {id: \"$version\"}}" >&3
fi;


