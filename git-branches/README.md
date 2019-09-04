# Resource for working with git branches matching a name pattern 

uploads and downloads REX releases

## Source Configuration

all the same options as https://github.com/concourse/git-resource except instead of branch
takes `filters` which is an array of values that will be fed to `git branch --list ...`

### Example

``` yaml
- name: rex-branches 
  type: git-branches 
  source:
    filters:
      - hotfix/*
      - testrelease/*
```

``` yaml
- get: rex-branches
```

## Behavior

### `check`: Check for new branches or updates.

returns mapping of branch names to commit shas

### `in`: Clone branches.

resource directory will have subdirectories for each branch name with the git 
files inside, helper files are created in there just like the default git resource.

`/` in branch names will be replaced with `-` in the directory names.

### `out`

not implemented
