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
