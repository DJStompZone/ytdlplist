# YT-DLPlist

This project is a Python application that manages YouTube playlist downloads.

## Project Structure

```
.gitignore
pyproject.toml
ytdlplist/
	data/
		playlists.template.json
	sounds/
        <sound files>.wav
	src/
		constants.py
		playlist_util.py
		utils.py
		ytdlplist.py
```

## Prerequisites

Poetry needs to be installed to install ytdlplist

```sh
pip install --upgrade poetry -q
```

## Setup

To set up the project, follow these steps:

1. Clone the repository.
2. Install the required dependencies using pip:

```sh
git clone https://github.com/DJStompZone/ytdlplist
cd ytdlplist
poetry install
```

## Usage

To run the application, navigate to the `src` directory and run the `ytdlplist.py` script:

```sh
poetry run src/ytdlplist.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)