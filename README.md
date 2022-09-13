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
``` sh
abstra configure [API_TOKEN]
```
Configures the current working directory credentials. Credentials are stored at `.abstra/credentials`.   

## Ignoring files

You can ignore files placing a `.abstraignore` at the target directory:
```
__pycache__
tests/
*.ipynb
```

`.abstraignore` itself will always be ignored

## Remote resources

Remote resources can be `files`, `vars` or `packages`.   
You can manage remote resources with the following commands:

### List resources
``` sh
abstra list RESOURCE
```
List remote resources on your workspace.   
Examples:
``` sh
abstra list packages
abstra list vars
abstra list files

# Saving envvars and packages
abstra list packages > requirements.txt
abstra list vars > .env
```

### Add resource
``` sh
abstra add RESOURCE [...OPTIONS]
```
Adds remote resources on your workspace.   
Examples:
``` sh
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
```

### Remove resource
``` sh
abstra remove RESOURCE [...OPTIONS]
```
Remove remote resources from your workspace.   
Examples:
``` sh
abstra remove files foo.txt bar.log
abstra remove vars ENVIROMENT VERSION
abstra remove packages pandas numpy scipy
```

### Aliases
Some commands have aliases.   

#### upload
``` sh
# Alias for `abstra add files` with default argument `.`
abstra upload [FILES or DIRECTORIES, default: .]
```

#### ls
``` sh
# Alias for `abstra list files`
abstra ls
```

#### rm
``` sh
# Alias for `abstra remove files`
abstra rm
```

#### install
``` sh
# Alias for `abstra add packages`
abstra install [PACKAGES]
```
