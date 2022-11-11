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

Most commands are authenticated. To authenticate you need to generate an API Token [here](https://forms.abstra.run/737986ce-a8ed-4c7b-bd7e-5f0b11331b66).

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
\*note: update and play commands are currently only available to the forms resource .
Remote resources can be `forms`, `files`, `vars` or `packages`.

You can manage remote resources with the following commands:

### List resources

```sh

abstra list RESOURCE{forms, files, vars, packages}

```

List remote resources on your workspace.

Examples:

```sh

abstra list packages

abstra list vars

abstra list files

abstra list forms


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

abstra add form --name="Form Name" --code "from hackerforms import * \n\ndisplay('hello_world')" --background '#fffeee' --main-color red --start-message 'start message' --error-message 'error-message' --end-message 'end message' --start-button-text 'start button text' --show-sidebar --allow-restart

```

### Update resource

_currently only available for forms_

````sh

```sh

abstra update [FORM_PATH] [...OPTIONS]

````

Updates remote resources on your workspace.

The current options for each resource are:

- forms:
  1.  `form_path`: string (required parameter)
  2.  `--name`: string
  3.  `--path`: string
  4.  `--file`: file_path
  5.  `--code`: string
  6.  `--background`: image_path or string
  7.  `--main-color`: string
  8.  `--start-message`: string
  9.  `--error-message`: string
  10. `--end-message`: string
  11. `--start-button-text`: string
  12. `--timeout-message`: string
  13. `--logo-url`: string
  14. `--show-sidebar`: boolean
  15. `--log-messages`: boolean
  16. `--font-color`: string
  17. `--auto-start`: boolean
  18. `--allow-restart`: boolean
  19. `--welcome-title`: string
  20. `--brand-name`: string

\*note: set either file or code, but not both.

Examples:

```sh

# Forms

abstra update form 7e549274-0e59-4b56-ad08-21bf48793be2 --name="Another name" --allow-restart
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

```

### Play resource

```sh

abstra play form 7e549274-0e59-4b56-ad08-21bf48793be2

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
