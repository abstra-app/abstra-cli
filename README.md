# abstra-cli

## Install
Download from pip (preferably using pipx):
```sh
pip[x] install abstra-cli
```



## Commands

Most commands are authenticated. To authenticate you need to request an API Token from [help@abstracloud.com](help@abstracloud.com).

### Configure
``` sh
abstra-cli configure API_TOKEN
```
Authenticates the CLI with the token. Stores credentials at `~/.abstra/config.json`.  
Optionally, you can set the `ABSTRA_API_TOKEN` environment variable.

### Upload
``` sh
abstra-cli upload DIRECTORY
```

### Ignoring files

you can ignore files placing a `.abstraignore` at the beginning of the filea:
```
__pycache__
tests/
*.ipynb
```

`.abstraignore` itself will always be ignored

**Requires authentication**  
Uploads the contents of the directory to the workspace. 
