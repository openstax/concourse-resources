# ZenHub Releases Resource

Fetches ZenHub Releases

## Source Configuration

* `token`: *Required.* ZenHub api token from [here](https://app.zenhub.com/dashboard/tokens).

* `repository_id`: *Required.* The repository id (which is different from the repo name, you can get this from the github api or the ZenHub dashboard url).

### Example

``` yaml
- name: zenhub-release
  type: zenhub-release
  source:
    repository_id: 12345565
    token: 78asd89asd89asd9s
```

``` yaml
- get: zenhub-release
```

To get a specific release id:

``` yaml
- get: zenhub-release
  version: {id : 'asdf89adsf78asdf' }
```

## Behavior

### `check`: Check for new releases.

Releases are listed by their release id

### `in`: Fetch release data.

fetches the given release, creating the following files:
* `release.json` the raw json from ZenHub.
* `id.txt` plaintext file with the release id
* `title.txt` plaintext file with the release title


### `out`

not implemented
