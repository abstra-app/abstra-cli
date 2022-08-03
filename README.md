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

## Upload
``` sh
abstra upload [DIRECTORY="."]
```
Uploads the current directory files (and recursively) in the configured workspace.   
Optionally, you can specify a directory to upload.

### Ignoring files

You can ignore files placing a `.abstraignore` at the directory that will be uploaded:
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
Example:
``` sh
abstra list packages
```

### Add resource
``` sh
abstra add RESOURCE [...OPTIONS]
```
Adds remote resources on your workspace.   
Example:
``` sh
abstra add files test.txt
abstra add vars ENVIROMENT=production VERSION=1.0.0
abstra add packages pandas numpy=1.0.1
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

#### install
``` sh
# Alias for `abstra add packages`
abstra install [PACKAGES]
```
