# YT-DLPlist

This project is a Python application that manages YouTube playlist downloads.

<img src="https://github.com/DJStompZone/ytdlplist/assets/85457381/fe0b684d-b1e6-4c24-a91c-4e9b53855fae">


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

Create your playlists file:

```sh
cp data/playlists.example.json data/playlists.json
```

Add your playlist urls to data/playlists.json, then run the application with:

```sh
poetry run start
```

## Project Structure

```
.gitignore
pyproject.toml
ytdlplist/
	data/
		playlists.template.json
		playlists.json
	sounds/
        	<sound files>.wav
	constants.py
	playlist_util.py
	utils.py
	ytdlplist.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
