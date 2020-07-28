# Stub Resource

allows tracking a version identifier accross concourse jobs without making a custom resource if you don't care about any upload/download logic


## Source Configuration
none

### Example

``` yaml
- name: environment-endpoint
  type: stub-resource
```


## Behavior

### `check`: Check for new releases.

check script does nothing for this resource

### `in`: Fetch release data.

``` yaml
- get: environment-endpoint 
```

whatever was stored in the version will end up at `environment-endpoint/version.txt`

### `out`

``` yaml
- put: environment-endpoint 
  params:
    file: path/to/file/with/something/in/it
```

the contents of the given file will be stored in the resource version. probably try to keep
it to a short string but i'm not actually sure when concourse will break.
