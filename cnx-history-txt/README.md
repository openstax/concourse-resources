# concourse-history-txt-resource

A Concourse CI resource for CNX webview history.txt versions.

## Source Configuration

* instance: _Required_ The instance of cnx.org ['dev', 'staging', 'prod']

### Example

```yaml
resource_types:
- name: history
  type: docker-image
  source:
    repository: openstax/concourse-history-txt-resource

resources:
- name: webview-history
  type: history
  source:
    instance: staging
```

## Development

### Configure Python Dev Environment

Create a virtualenv:

`python3 -m venv .venv`

Install dependencies:

`pip install .[dev]`

### Run unit tests

`pytest -vvv tests/`

### Build the docker image

Create a distribution:

`python setup.py sdist`

Build the image:

`docker build -t user/concourse-history-txt-resource .`
