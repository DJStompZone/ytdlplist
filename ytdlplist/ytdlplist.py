import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from os import name as osname
from os import path, system
from types import ModuleType
from typing import Callable, Coroutine, Literal

from ytdlplist.constants import BANNER, RESET, YELLOW
from ytdlplist.playlist_util import Playlist
from ytdlplist.utils import find_data_dir, find_sound

executor = ThreadPoolExecutor(max_workers=1)


wave: ModuleType | None = None
pyaudio: ModuleType | None = None

sound_enabled = False


def sound_init():
    global sound_enabled, wave, pyaudio
    try:
        wave = __import__("wave")

        pyaudio = __import__("pyaudio")

        sound_enabled = True
    except ImportError:
        pass


async def __play_sound(sound_file: str) -> None:
    """
    Play a sound file.

    Parameters
    ----------
    sound_file : str
        Path to the sound file to play.
    """
    global sound_enabled
    if not sound_enabled:
        return

    def _play_sound(sound_file: str):
        global sound_enabled, pyaudio, wave
        try:
            sound_file = find_sound(sound_file)
        except FileNotFoundError:
            sound_enabled = False
            return
        if sound_enabled and pyaudio and wave:
            chunk: Literal[1024] = 1024
            f = wave.open(sound_file, "rb")
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True,
            )
            data: bytes = f.readframes(chunk)
            while data:
                stream.write(data)
                data = f.readframes(chunk)
            stream.stop_stream()
            stream.close()
            p.terminate()

    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, _play_sound, sound_file)


def get_sound_player() -> Callable[..., Coroutine[str, None, None]]:
    """
    Get the sound player coroutine.

    Returns
    -------
    Coroutine
        The sound player coroutine.
    """

    async def dummy_player(sound_file: str) -> None:
        pass

    return __play_sound if sound_enabled else dummy_player


async def play_sound(sound_file: str) -> None:
    """
    Play a sound file.

    Parameters
    ----------
    sound_file : str
        Path to the sound file to play.

    Raises
    ------
    FileNotFoundError
        If the sound file does not exist.
    """
    await get_sound_player()(sound_file)


async def dlplist_main(
    playlists: list[str],
    player: Callable[..., Coroutine[str, None, None]] | None = None,
) -> None:
    # Create the tasks
    sound_task = asyncio.create_task(play_sound("ps1.wav"))
    banner_task = asyncio.create_task(abanner())
    await asyncio.gather(sound_task, banner_task)

    for _playlist in playlists:
        playlist = Playlist(_playlist, player or get_sound_player())
        await playlist.async_init()
        pname: str = playlist.title.replace(" ", "_")
        outdir: str = path.join(
            path.expanduser("~"), "Music", "yt-dlp", "Playlists", pname
        )
        await playlist.download(
            audio_only=True,
            output_dir=outdir,
            output_ext="mp3",
            interval=30,
        )


def banner():
    print(
        YELLOW,
        "\n",
        __import__("base64").b64decode(BANNER).decode("u16"),
        RESET,
        sep="",
    )


async def abanner():
    await asyncio.sleep(1.5)
    banner()


def main():
    system("cls" if osname == "nt" else "clear")
    sound_init()
    PLAYER = get_sound_player()
    _playlists: list[Playlist] = []
    with open(path.join(find_data_dir(), "playlists.json"), "r") as fp:
        plists: list[str] = Playlist.validate_playlists(json.load(fp))
        asyncio.run(dlplist_main(playlists=plists, player=PLAYER))


if __name__ == "__main__":
    main()
