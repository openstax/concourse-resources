#!/usr/bin/env python3

# Creates the S3 redirects for a REX release
#
# Usage: redirects.py BUCKET VERSION REDIRECTS_JSON
#
# Checks every redirect first, before creating any of them. A redirect that already exists with
# the same target is skipped, so a release whose upload failed partway can be uploaded again.
# Then creates them in parallel with one shared S3 client so we don't pay the python startup cost per object.

import json
import sys
from concurrent.futures import ThreadPoolExecutor

import botocore.session
from botocore.config import Config

CONCURRENCY = 32


def list_keys(s3, bucket, prefix):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get('Contents', []):
            yield item['Key']


def redirect_locations_by_key(s3, bucket, keys, executor):
    def redirect_location(key):
        # Objects that aren't redirects have no WebsiteRedirectLocation
        return s3.head_object(Bucket=bucket, Key=key).get('WebsiteRedirectLocation')

    return dict(zip(keys, executor.map(redirect_location, keys)))


def find_errors(redirects, release_prefix, existing_keys, existing_locations_by_key):
    errors = []
    created_paths = set()

    for redirect in redirects:
        from_path = redirect['from']
        to = redirect['to']
        from_key = release_prefix + from_path
        # The target file is the target without its query string
        to_path = to.rsplit('?', 1)[0]

        if from_path in created_paths:
            errors.append('cannot create redirection from {} to {}: {} is redirected twice'.format(
                from_path, to, from_path))
        # An earlier upload of this release may have created the same redirect already. Anything
        # else at that path, such as an uploaded file or a different redirect, is an error.
        elif from_key in existing_keys and existing_locations_by_key[from_key] != to:
            errors.append('cannot create redirection from {} to {}: {} already exists'.format(
                from_path, to, from_path))
        # Only targets under /books must exist, either as an uploaded file or as a redirect
        # created earlier in this run
        elif (to.startswith('/books') and to_path not in created_paths and
              release_prefix + to_path not in existing_keys):
            errors.append('cannot create redirection from {} to {}: {} does not exist'.format(
                from_path, to, to_path))

        created_paths.add(from_path)

    return errors


def main(bucket, version, redirects_path):
    release_prefix = 'rex/releases/' + version

    with open(redirects_path) as redirects_file:
        redirects = json.load(redirects_file)

    s3 = botocore.session.get_session().create_client(
        's3', config=Config(max_pool_connections=CONCURRENCY))

    existing_keys = set(list_keys(s3, bucket, release_prefix + '/'))

    def create_redirect(redirect):
        s3.put_object(Bucket=bucket, Key=release_prefix + redirect['from'],
                      WebsiteRedirectLocation=redirect['to'])

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        existing_from_keys = [release_prefix + redirect['from'] for redirect in redirects
                              if release_prefix + redirect['from'] in existing_keys]
        existing_locations_by_key = redirect_locations_by_key(
            s3, bucket, existing_from_keys, executor)

        errors = find_errors(redirects, release_prefix, existing_keys, existing_locations_by_key)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            print('aborting without creating any redirects', file=sys.stderr)
            sys.exit(1)

        new_redirects = [redirect for redirect in redirects
                         if release_prefix + redirect['from'] not in existing_keys]

        print('creating {} redirects ({} already exist)'.format(
            len(new_redirects), len(redirects) - len(new_redirects)), file=sys.stderr)

        # Consuming the results raises the first failed request's error
        for _ in executor.map(create_redirect, new_redirects):
            pass

    print('created {} redirects'.format(len(new_redirects)), file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: {} BUCKET VERSION REDIRECTS_JSON'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    main(*sys.argv[1:])
