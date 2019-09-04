#!/bin/bash
set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

# shellcheck disable=SC1090
source "$(dirname "$0")/common.sh"

# for jq
PATH=/usr/local/bin:$PATH

payload=$TMPDIR/git-resource-request

cat > "$payload" <&0

load_pubkey "$payload"
configure_https_tunnel "$payload"
configure_git_ssl_verification "$payload"
configure_credentials "$payload"

uri=$(jq -r '.source.uri // ""' < "$payload")
read -ra list_arg <<< "$( jq -r '(.source.filters // []) | map("origin/" + .) | join(" ")' < "$payload")"
git_config_payload=$(jq -r '.source.git_config // []' < "$payload")

configure_git_global "${git_config_payload}"

destination=$TMPDIR/git-resource-repo-cache

if [ -d "$destination" ]; then
  cd "$destination"
  git fetch -f
  git reset --hard FETCH_HEAD
else
  git clone "$uri" "$destination"
  cd "$destination"
fi

branches=$(git branch -r --list "${list_arg[@]}" --format '%(refname:lstrip=3) %(objectname:short)')
formatted=$(echo "$branches" | jq --slurp --raw-input 'split("\n")[:-1] | map([ split(" ")[] ]) | map(join(":")) | join(",") | [{refs: .}]')

echo "$formatted" >&3
