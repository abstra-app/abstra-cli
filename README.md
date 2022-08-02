# abstra-cli

## Install
Download from pip (preferably using pipx):
```sh
pip[x] install abstra-cli
```

## Commands

Most commands are authenticated. To authenticate you need to generate an API Token [here](https://forms.abstra.run/737986ce-a8ed-4c7b-bd7e-5f0b11331b66).   
Authentication credentials are stored in the current directory at `.abstra/credentials`.   
Alternatively you can set the `ABSTRA_API_TOKEN` environment variable.   

### Configure
``` sh
abstra configure [API_TOKEN]
```
Configures the current working directory credentials. Credentials are stored at `.abstra/credentials`.   

### Upload
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

**Requires authentication**  
Uploads the contents of the directory to the workspace. 
