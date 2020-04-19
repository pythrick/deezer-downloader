# Deezer Downloader
Bot to download mp3 songs from YouTube based on my Deezer favorites tracks.

* The current process involves calling different scripts from this project.


## Requirements
- Deezer APP API
  - Go to Deezer developers website: https://developers.deezer.com
  - Login with your standard Deezer account, and go to My App.
  - Create an application id for your project by clicking on "Create a new application" button
  - Fill in the app creation form and validate. You can edit your application later to add additional informations.
  
- Authenticate using Deezer Oauth flow to get your ACCESS_TOKEN
  - Follow these instructions: https://developers.deezer.com/api/oauth
  - Store the new access_token as a secret:
    ```bash
    poetry run dynaconf write toml -s ACCESS_TOKEN=YOUR_ACESS_TOKEN
    ```
  
  
## Install
This project uses Poetry to manage its dependencies, if you're not familiar about using `poetry` you can find the 
installation instructions on the following links: 
- [Poetry - Installation](https://python-poetry.org/docs/#installation)
- [Poetry - Basic Usage](https://python-poetry.org/docs/basic-usage/#basic-usage)

### Installing project dependencies
```bash
poetry install
```

## Usage
All the following scripts are done calling scripts from command line.

### Consummer
Consumes Deezer API and get list of my favorite tracks and stores in database
```bash
poetry run python consumer.py
```

### Searcher
Searches for tracks on youtube and stores the results in database

```bash
poetry run python seacher.py
```

### Downloader
Downloads tracks from Youtube in `mp3` format
```bash
poetry run python downloader.py
```
  
### Filler
Fills the `id3` tags inside tracks
```bash
poetry run python filler.py
```

## Disclaimer
Downloading copyrighted material may be illegal in your country. Use at your own risk.


## The MIT License
Copyright (c) 2020 Patrick Rodrigues https://github.com/pythick

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
