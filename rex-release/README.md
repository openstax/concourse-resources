# REX Releases Resource

uploads and downloads REX releases

## Source Configuration

* `bucket`: *Required.* The REX release bucket. eg: 'unified-web-primary'.

* `access_key_id`: *Required.* AWS access key id that permission to do stuff to the target bucket.

* `secret_access_key`: *Required.* AWS secret access key for the specified id.

* `prefix`: *optional.* Limit releases to those that match a certain prefix. eg: 'master'.

### Example

``` yaml
- name: rex-release 
  type: rex-release 
  source:
    access_key_id: asdf
    secret_access_key: asdf
    prefix: master
```

``` yaml
- get: rex-release
```

To get a specific release id:

``` yaml
- get: rex-release
  version: {id: 'master/a90sd09s' }
```

## Behavior

### `check`: Check for new releases.

Sorted by modified date because s3 doesn't track created date. this is probably fine because rex releases are not updated.

### `in`: Fetch release data.

for now only the `rex/release.json` file is downloaded.

### `out`

``` yaml
- put: rex-release
  params:
    path: path/to/release/files
```
