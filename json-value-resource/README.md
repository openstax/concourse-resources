# Stub Resource

fetches a json file from the internet and extracts a value to use as its version using the "jq" language

## Source Configuration
* `url`: *Required.* The url to fetch json from.

* `fn`: *Required.* jq language function to use to extract version eg: `.version` 

### Example

``` yaml
- name: environment-version
  type: json-value-resource
  source:
    url: https://openstax.org/rex/release.json
    fn: .code
```


## Behavior

### `check`: Check for new versions.

fetches the url and publishes new versions to concourse.

### `in`: Writes version string to file.

``` yaml
- get: environment-version 
```

whatever was stored in the version will end up at `environment-version/version.txt`

### `out`

``` yaml
- put: environment-version
  params:
    file: path/to/file/with/something/in/it
```

the contents of the given file will be stored in the resource version (in concourse only).
