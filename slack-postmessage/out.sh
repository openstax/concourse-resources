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

payload=$(mktemp /tmp/resource-out.XXXXXX)

cat > "$payload" <&0

text_file=$(jq -r '.params.text_file | select (.!=null)' < "$payload")
text=$(jq -r '.params.text | select (.!=null)' < "$payload")
thread=$(jq -r '.params.thread | select (.!=null)' < "$payload")
slack_token=$(jq -r '.source.slack_token | select (.!=null)' < "$payload")
slack_user=$(jq -r '.source.slack_user | select (.!=null)' < "$payload")
slack_channel=$(jq -r '.source.slack_channel | select (.!=null)' < "$payload")

if [ -z "$text" ] && [ -n "$text_file" ] && [ -f "$text_file" ]; then
  text=$(<"$text_file")
fi

if [ -z "$text" ]; then
  echo "text for the slack message is required"
  exit 1;
fi

post_args=( \
  --data-urlencode "token=$slack_token" \
  --data-urlencode "as_user=$slack_user" \
  --data-urlencode "link_names=true" \
  --data-urlencode "channel=$slack_channel" \
  --data-urlencode "text=$text" \
)

if [ -f "$thread/version.txt" ]; then
  thread_id=$(<"$thread/version.txt")
  post_args+=(--data-urlencode "thread_ts=$thread_id")
  echo "found version.txt with $thread_id, using that"
else
  echo "no version.txt found, starting new thread"
fi

post_response=$(curl -s -X POST https://slack.com/api/chat.postMessage "${post_args[@]}")

if [ -n "${thread_id+x}" ]; then
  jq -n --arg thread_id "$thread_id" '{version: {id: $thread_id}}' >&3
else
  jq "{version: {id: .message.ts}}" <<< "$post_response" >&3
fi
