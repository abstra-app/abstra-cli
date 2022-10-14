[![pypi](https://img.shields.io/pypi/v/abstra-cli.svg)](https://pypi.python.org/pypi/abstra-cli)

[![PyPI Downloads](https://img.shields.io/pypi/dm/abstra-cli.svg)](

https://pypi.org/project/abstra-cli/)

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
  1.  \-\-name: string
  2.  \-\-file\*: file_path
  3.  \-\-code\*: string
  4.  \-\-background: image_path or string
  5.  \-\-main-color: string
  6.  \-\-start-message: string
  7.  \-\-error-message: string
  8.  \-\-end-message: string
  9.  \-\-start-button-text: string
  10. \-\-timeout-message: string
  11. \-\-logo-url: string
  12. \-\-show-sidebar: boolean
  13. \-\-log-messages: boolean
  14. \-\-font-color: string
  15. \-\-auto-start: boolean
  16. \-\-allow-restart: boolean
  17. \-\-welcome-title: string
  18. \-\-brand-name: string

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

### Update form

```sh

abstra add RESOURCE [...OPTIONS]

```

Adds remote resources on your workspace.

The current options for each resource are:

- forms:
  1.  form_id: string (required parameter)
  2.  \-\-name: string
  3.  \-\-file\*: file_path
  4.  \-\-code\*: string
  5.  \-\-background: image_path or string
  6.  \-\-main-color: string
  7.  \-\-start-message: string
  8.  \-\-error-message: string
  9.  \-\-end-message: string
  10. \-\-start-button-text: string
  11. \-\-timeout-message: string
  12. \-\-logo-url: string
  13. \-\-show-sidebar: boolean
  14. \-\-log-messages: boolean
  15. \-\-font-color: string
  16. \-\-auto-start: boolean
  17. \-\-allow-restart: boolean
  18. \-\-welcome-title: string
  19. \-\-brand-name: string

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

abstra remove form 7e549274-0e59-4b56-ad08-21bf48793be2

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
