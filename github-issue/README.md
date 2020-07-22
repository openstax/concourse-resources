# Github Issue Resource

Fetches Github Issue

## Source Configuration

* `token`: *Required.* github token.

* `repository`: *Required.* The repository name [organization/name].

* `params`: _optional._ Any parameter except since, direction, or sort from https://developer.github.com/v3/issues/#parameters-3

### Example

``` yaml
- name: github-issue
  type: github-issue
  source:
    repository: 'org/repo'
    token: 'token'
    params:
      labels: release
```

``` yaml
- get: github-issue
```

## Behavior

### `check`: Check for new issues.

Checks to see if any issues have been updated or created, and if so, passes to `in`. 

### `in`: Fetch issue data.

fetches the given issue, creating the following files:
* `issue.json` the raw json from Github.
* `number.txt` plaintext file with the issue number
* `title.txt` plaintext file with the issue title
* `body.txt` plaintext file with the issue body

### `out`

not implemented
