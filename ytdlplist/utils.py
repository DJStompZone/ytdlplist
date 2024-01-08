import os


def find_data_dir() -> str:
    """
    Find the data directory.

    Returns
    -------
    str
        The path to the data directory.

    Raises
    ------
    FileNotFoundError
        If the data directory is not found.
    """

    def __has_json_files(pth: str) -> bool:
        if not os.path.exists(pth):
            return False
        return any(fn.endswith(".json") for fn in os.listdir(pth))

    for _i in range(2):
        test_path = os.path.realpath(
            os.path.join(
                os.path.realpath(os.getcwd()), "ytdlplist", *[".."] * _i, "data"
            )
        )
        if os.path.exists(test_path) and __has_json_files(test_path):
            target = os.path.realpath(test_path)
            return target
    raise FileNotFoundError("Data directory not found.")


def ensure_valid_destination(path: str) -> int:
    """
    Check if a path is a valid destination and create it if it does not exist.

    Parameters
    ----------
    path : str
        Path to check.

    Returns
    -------
    int
        0 if the path is a valid destination.

    Raises
    ------
    OSError
        If the path is not a valid destination.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.isdir(path):
            raise OSError("Output directory does not exist.")
        return 0
    except Exception as e:
        raise OSError(
            "Error creating output directory. Please check your permissions."
        ) from e


def find_sound(sound_file: str) -> str:
    """
    Find a sound file.

    Parameters
    ----------
    sound_file : str
        Name of the sound file to find.

    Returns
    -------
    str
        Path to the sound file.

    Raises
    ------
    FileNotFoundError
        If the sound file is not found.
    """
    data_path: str = find_data_dir()
    if not os.path.exists(data_path):
        if os.path.exists(os.path.join(os.getcwd(), "data")):
            data_path = os.path.join(os.getcwd(), "data")
    soundpath: str = os.path.join(data_path, os.path.pardir, "sounds", sound_file)
    if os.path.exists(soundpath):
        return soundpath
    else:
        raise FileNotFoundError("Sound file not found.")
