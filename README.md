[![pypi](https://img.shields.io/pypi/v/abstra-cli.svg)](https://pypi.python.org/pypi/abstra-cli)

[![PyPI Downloads](https://img.shields.io/pypi/dm/abstra-cli.svg)](https://pypi.org/project/abstra-cli/)

[![Code check](https://github.com/abstra-app/abstra-cli/actions/workflows/code_check.yml/badge.svg)](https://github.com/abstra-app/abstra-cli/actions/workflows/code_check.yml)

# abstra-cli

# Install

Download from pip (preferably using pipx):

```sh

pip[x] install abstra-cli

```

# Commands

Most commands are authenticated. To authenticate you need to generate an API Token [here](https://forms.abstra.run/generate-token).

Authentication credentials are stored in the current directory at `.abstra/credentials`.

Alternatively you can set the `ABSTRA_API_TOKEN` environment variable.

## Configure

```sh

abstra configure [API_TOKEN]

```

It configures the current working directory credentials. Credentials are stored at `.abstra/credentials`.

## Ignoring files

You can ignore files placing a `.abstraignore` at the target directory:

```

__pycache__

tests/

*.ipynb

```

`.abstraignore` itself will always be ignored

## Remote resources

The general structure of the commands follows the pattern below:
usage: abstra \<command> \<resource> [\<argument>...] [--\<optional-argument-name> \<optional-argument-value> ...]

The available commands are: list, add, update*, remove and play*.
\*note: update and play commands are currently only available for forms and hooks .
Remote resources can be `forms`, `hooks`, `jobs`, `files`, `vars` or `packages`.

You can manage remote resources with the following commands:

### List resources

```sh

abstra list RESOURCE{forms, hooks, jobs, files, vars, packages}

```

List remote resources on your workspace.

Examples:

```sh

abstra list packages

abstra list vars

abstra list files

abstra list forms

abstra list hooks

abstra list jobs

# Saving env vars and packages

abstra list packages > requirements.txt

abstra list vars > .env

```

### Add resource

```sh

abstra add RESOURCE [...OPTIONS]

```

Adds remote resources on your workspace.

The current options for each resource are:

- forms:
  1.  `--name` or `--n` or `--title`: string
  1.  `--path`: string
  1.  `--file` or `--f`: file_path
  1.  `--code` or `--c`: string
  1.  `--enabled`: boolean
  1.  `--background`: image_path or string
  1.  `--main-color`: string
  1.  `--start-message`: string
  1.  `--error-message`: string
  1.  `--end-message`: string
  1.  `--start-button-text`: string
  1.  `--timeout-message`: string
  1.  `--logo-url`: string
  1.  `--show-sidebar`: boolean
  1.  `--log-messages`: boolean
  1.  `--font-color`: string
  1.  `--auto-start`: boolean
  1.  `--allow-restart`: boolean
  1.  `--welcome-title`: string
  1.  `--brand-name`: string
  1.  `--upsert`: boolean

\*note: set either file or code, but not both.

- hooks:
  1.  `--name` or `--n` or `--title`: string
  1.  `--path`: string
  1.  `--file` or `--f`: file_path
  1.  `--code` or `--c`: string
  1.  `--enabled`: boolean
  1.  `--upsert`: boolean

\*note: set either file or code, but not both.

- jobs:
  1.  `--name` or `--n` or `--title`: string
  1.  `--identifier` or `--idt`: string
  1.  `--schedule` or `--crontab`: string
  1.  `--file` or `--f`: file_path
  1.  `--code` or `--c`: string
  1.  `--enabled`: boolean
  1.  `--upsert`: boolean

\*note: set either file or code, but not both.

- files:

  1. file_path[]: list of file or directory paths

- vars:

  1.  environment_variable[]: list of Key=Value env vars
  2.  -f or \-\-file: file_path (ex. -f .env)

- packages:
  1. package_name[]: list of packages with optional version (ex. numpy=1.0.1)
  2. -f or \-\-file: file_path (ex. --file requirements.txt)

Examples:

```sh

# Files

abstra add files foo.txt bar.log

abstra add files foo/ ./



# Vars

abstra add vars ENVIROMENT=production VERSION=1.0.0

abstra add vars -f .env

abstra add vars --file .env



# Packages

abstra add packages pandas numpy=1.0.1 scipy>=1.0.1

abstra add packages -f requirements.txt

abstra add packages -r requirements.txt

abstra add packages --file requirements.txt

abstra add packages --requirement requirements.txt


# forms

abstra add form --name="my_form" -f main.py --background '#fffeee'

abstra add form --path=test -f test.py --enabled=False

abstra add form --name="Form Name" --code "from hackerforms import * \n\ndisplay('hello_world')" --background '#fffeee' --main-color red --start-message 'start message' --error-message 'error-message' --end-message 'end message' --start-button-text 'start button text' --show-sidebar --allow-restart


# hooks

abstra add hook --name="test hook" -f main.py --upsert

abstra add hook --path=test -f test.py --enabled=False

# jobs

abstra ad job --idt new-job --noenabled --name="Test Job" --upsert

abstra ad job --idt daily --schedule="00 00 00 * *" --name="Every midnight"

```

### Update resource

_currently only available for forms, hooks and jobs_

````sh

```sh

abstra update [IDENTIFIER OR PATH] [...OPTIONS]

````

Updates remote resources on your workspace.

The current options for each resource are:

- forms:

  1.  `form_path`: string (required parameter)
  2.  `--name`: string
  3.  `--path`: string
  4.  `--file`: file_path
  5.  `--code`: string
  6.  `--enabled`: boolean
  7.  `--background`: image_path or string
  8.  `--main-color`: string
  9.  `--start-message`: string
  10. `--error-message`: string
  11. `--end-message`: string
  12. `--start-button-text`: string
  13. `--timeout-message`: string
  14. `--logo-url`: string
  15. `--show-sidebar`: boolean
  16. `--log-messages`: boolean
  17. `--font-color`: string
  18. `--auto-start`: boolean
  19. `--allow-restart`: boolean
  20. `--welcome-title`: string
  21. `--brand-name`: string

- hooks:

  1.  `hook_path`: string (required parameter)
  1.  `--name` or `--n` or `--title`: string
  1.  `--path`: string
  1.  `--file` or `--f`: file_path
  1.  `--code` or `--c`: string
  1.  `--enabled`: boolean

- jobs:
  1.  `identifier`: string (required parameter)
  1.  `--name` or `--n` or `--title`: string
  1.  `--identifier` or `--idt`: string
  1.  `--schedule` or `--crontab`: string
  1.  `--file` or `--f`: file_path
  1.  `--code` or `--c`: string
  1.  `--enabled`: boolean

Examples:

```sh

# Forms

abstra update form new-onboarding --name="Another name" --allow-restart

abstra update hook stripe-callback --enabled

abstra update job daily --schedule="00 00 5 * *"
```

### Remove resource

```sh

abstra remove RESOURCE [...OPTIONS]

```

Remove remote resources from your workspace.

Examples:

```sh

abstra remove files foo.txt bar.log

abstra remove vars ENVIROMENT VERSION

abstra remove packages pandas numpy scipy

abstra remove form sales-onboarding

abstra remove hook stripe-test

abstra remove job monthly

```

### Play resource

```sh

abstra play form b2b-ingestion

abstra play hook hasura-callback --method POST

```

### Aliases

Some commands have aliases.

#### upload

```sh

# Alias for `abstra add files` with default argument `.`

abstra upload [FILES or DIRECTORIES, default: .]

```

#### ls

```sh

# Alias for `abstra list files`

abstra ls

```

#### rm

```sh

# Alias for `abstra remove files`

abstra rm

```

#### install

```sh

# Alias for `abstra add packages`

abstra install [PACKAGES]

```
