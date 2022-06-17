# abstra-cli

## Install
Download from pip (preferably using pipx):
```sh
pip[x] install abstra-cli
```



## Commands

### Configure
``` sh
abstra-cli configure API_TOKEN
```
Authenticates the CLI with the token. Stores credentials at `~/.abstra/config.json`.

### Upload
``` sh
abstra-cli upload DIRECTORY
```
Uploads the contents of the directory to the workspace. 