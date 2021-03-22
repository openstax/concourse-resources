# Github Milestone Resource

Fetches Github Milestone

## Source Configuration

* `token`: *Required.* github token.

* `repository`: *Required.* The repository name [organization/name].

* `mode`: *optional.* default *single*, specify *multiple* to use all open milestones as one resource.

### Example

``` yaml
- name: github-milestone
  type: github-milestone
  source:
    repository: org/repo
    token: abcdtoken
```

``` yaml
- get: github-milestone
```

To get a specific milestone number:

``` yaml
- get: github-milestone
  version: {id : '5' }
```

## Behavior

### `check`: Check for new milestones.

Milestones are listed by their number

### `in`: Fetch milestone data.

fetches the given milestone, creating the following files:
* `milestone.json` the raw json from Github.
* `id.txt` plaintext file with the milestone id
* `number.txt` plaintext file with the milestone number
* `title.txt` plaintext file with the milestone title
* `title-slug.txt` plaintext file with the milestone title but slugified

if `source.mode` is set to *multiple* then these files are all generated in folders corresponding to the milestone number.

### `out`

not implemented
