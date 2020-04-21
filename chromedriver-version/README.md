# chromedriver-version

## Examples

```yaml
resource_types:
  - name: chromedriver-version
    type: docker-image
    source:
      repository: openstax/chromedriver-version-resource

resources:
  - name: chromedriver-latest
    type: chrome-driver-version

```

## `get`: Get the latest version of chromedriver

### Files created

* `version`: A file that contains the version

### Example

```yaml
plan:
  - get: chromedriver-latest
    trigger: true
```

## `put`:

Not Implemented


## Configure Dev Environment

Create a virtualenv:

`python3 -m venv .venv`

Activate the virtualenv:

`sourcee ./.venv/bin/activate`

Install dependencies:

`pip install .[dev]`

### Run unit tests

`make test`

### Build the docker image for development

`make build-image`

### Build the docker image tagged latest

`make tag-latest`

### Release the versioned image to dockerhub

`make release`

### Release the latest image to dockerhub

`make release-latest`
