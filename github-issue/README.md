# Github Issue Resource

Fetches Github Issue

## Source Configuration

* `token`: *Required.* github token.

* `repository`: *Required.* The repository name [organization/name].

* `version: {"number": <issue number> , "modified": <last modified date of issue>}`: 

### Example

``` yaml
- name: github-issue
  type: github-issue
  source:
    repository: 'org/repo'
    token: 'token'
  version: {"number": <number> , "modified": <date>}
```

``` yaml
- get: github-issue
```

## Behavior

### `check`: Check for new issues.

Checks to see if an issue has been updated recently, and if so, passes to `in`. You can specify a specific issue if needed as 

A version can be passed in if needed. 

### `in`: Fetch issue data.

fetches the given issue, creating the following files:
* `issue.json` the raw json from Github.
* `number.txt` plaintext file with the issue number
* `title.txt` plaintext file with the issue title
* `body.txt` plaintext file with the issue body

### `out`

not implemented
