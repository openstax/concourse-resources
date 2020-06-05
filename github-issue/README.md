# Github Issue Resource

Fetches Github Issue

## Source Configuration

* `token`: *Required.* github token.

* `repository`: *Required.* The repository name [organization/name].

* `number`: *Required.* The Github issue number to fetch

* `version: {date: }`: *Required.* A blank list for dates for the resource to trigger on.

### Example

``` yaml
- name: github-issue
  type: github-issue
  source:
    repository: 'org/repo'
    token: 'token'
    number '1234'
    version: {date : ''}
```

``` yaml
- get: github-issue
```

## Behavior

### `check`: Check for new issues.

Checks to see if the `updated_at` timestamp is newer than previous. 

### `in`: Fetch issue data.

fetches the given issue, creating the following files:
* `issue.json` the raw json from Github.
* `number.txt` plaintext file with the issue number
* `title.txt` plaintext file with the issue title
* `body.txt` plaintext file with the issue body

### `out`

not implemented
