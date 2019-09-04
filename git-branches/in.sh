#!/bin/bash
set -e -u

exec 3>&1 # make stdout available as fd 3 for the result
exec 1>&2 # redirect all output to stderr for logging

# shellcheck disable=SC1090
source "$(dirname "$0")/common.sh"

destination=$1

if [ -z "$destination" ]; then
  echo "usage: $0 <path/to/destination>" >&2
  exit 1
fi

# for jq
PATH=/usr/local/bin:$PATH

payload=$(mktemp "$TMPDIR"/git-resource-request.XXXXXX)

cat > "$payload" <&0

load_pubkey "$payload"
configure_https_tunnel "$payload"
configure_git_ssl_verification "$payload"
configure_credentials "$payload"

uri=$(jq -r '.source.uri // ""' < "$payload")
git_config_payload=$(jq -r '.source.git_config // []' < "$payload")
short_ref_format=$(jq -r '(.params.short_ref_format // "%s")' < "$payload")
refs=$(jq -r '.version.refs // ""' < "$payload")

configure_git_global "${git_config_payload}"

checkout=$(mktemp -d "$TMPDIR"/git-resource-request-checkout.XXXXXX)

git clone "$uri" "$checkout"

IFS=',' read -ra refs_array <<< "$refs"
for ref in "${refs_array[@]}"; do
  IFS=':' read -ra ref_array <<< "$ref"
  name=${ref_array[0]}
  sha=${ref_array[1]}

  ref_destination="$destination/$name";

  mkdir -p "$ref_destination"

  git clone "$checkout" "$ref_destination"

  cd "$ref_destination"

  git checkout -q "$sha"
  git clean -f

  # Store committer email in .git/committer. Can be used to send email to last committer on failed build
  # Using https://github.com/mdomke/concourse-email-resource for example
  git --no-pager log -1 --pretty=format:"%ae" > .git/committer

  # Store git-resource returned version ref .git/ref. Useful to know concourse
  # pulled ref in following tasks and resources.
  echo "$ref" > .git/ref

  # Store short ref with templating. Useful to build Docker images with
  # a custom tag
  echo "$ref" | cut -c1-7 | awk "{ printf \"${short_ref_format}\", \$1 }" > .git/short_ref

  # Store commit message in .git/commit_message. Can be used to inform about
  # the content of a successfull build.
  # Using https://github.com/cloudfoundry-community/slack-notification-resource
  # for example
  git log -1 --format=format:%B > .git/commit_message
done

jq -n "{
  version: {refs: \"$refs\"}
}" >&3
