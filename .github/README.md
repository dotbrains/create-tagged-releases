# create-tagged-releases

## Overview

This script creates a tagged Github release for all repositories listed in `config.yml`

## Requirements

- Python 3.6+
- Poetry
- A Github personal access token with `repo` scope

## Installation

```shell
poetry install
```

## Configuration

Replace the values in `.env` with your own.

```shell
cp .env.example .env
```

Change the values in `config.yml` to match your repositories.

```yaml
access_token: ${GITHUB_ACCESS_TOKEN}
repo:
  org: organization-name
  names:
    - service-name
release:
  branch: main
```

## Usage

```shell
create-tagged-releases.py [-h] [--tag TAG]
```

## Docker

```shell
docker build -t create-tagged-releases .
docker run --rm --env-file .env create-tagged-releases --tag 1.0.0
```
