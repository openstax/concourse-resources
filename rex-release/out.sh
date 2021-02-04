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
checkout=$(jq -r '.params.checkout | select (.!=null)' < "$payload")
bucket=$(jq -r '.source.bucket | select (.!=null)' < "$payload")
aws_access_key_id=$(jq -r '.source.access_key_id' < "$payload")
aws_secret_access_key=$(jq -r '.source.secret_access_key' < "$payload")
export AWS_ACCESS_KEY_ID=$aws_access_key_id
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

upload-release() {
  path=$1
  version=$2

  if [ -z "$path" ]; then
    echo "path must be provided"
    exit 1;
  fi

  if aws s3api get-object --bucket "$bucket" --key "rex/releases/$version/rex/release.json" /dev/null > /dev/null 2>&1; then
    echo "release $version already exists, aborting"
    exit 1;
  fi;

  for row in $(jq -c '.[]' < $path/rex/redirects.json); do
    from=$(jq -r '.from' <<< "$row")
    to=$(jq -r '.to' <<< "$row")

    if [ ! -e "$path/$from" ] && [ -e "$path/$to" ]; then
      echo "cannot create redirection from $from to $to, aborting"
      exit 1;
    fi
  done

  # everything outside books gets uploaded nicely and can have long cache becaue it is loaded from versioned url
  aws s3 sync --exclude 'books/*' --cache-control 'max-age=31536000'  "$path" "s3://$bucket/rex/releases/$version"

  # service worker uploaded separately to have the right content-type, loaded unversioned so no cloudfront caching
  aws s3 sync --exclude '*' --include 'service-worker.js' --cache-control 'max-age=0'  "$path/books/" "s3://$bucket/rex/releases/$version/books"

  # books files with explicit content type set because they don't have extensions, loaded unversioned so no cloudfront caching
  aws s3 sync --exclude 'service-worker.js' --content-type 'text/html' --cache-control 'max-age=0' "$path/books/" "s3://$bucket/rex/releases/$version/books"

  # configure redirects
  for row in $(jq -c '.[]' < $path/rex/redirects.json); do
    from=$(jq -r '.from' <<< "$row")
    to=$(jq -r '.to' <<< "$row")
    aws s3api put-object --bucket "$bucket" --key "$from" --website-redirect-location "$to"
  done
}


if [ "$checkout" ]; then
  jq -n "{version: {id: \"$checkout\"}}" >&3
else
  version=$(jq -r '.id | select (.!=null)' < "$dir"/rex/release.json)
  upload-release "$dir" "$version"
  jq -n "{version: {id: \"$version\"}}" >&3
fi;


