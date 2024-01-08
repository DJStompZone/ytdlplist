import asyncio
import json
import re
import subprocess
import time
from subprocess import CalledProcessError
from typing import Any, Callable, Coroutine

from ytdlplist.constants import DARK, GREEN, MAGENTA, RED, RESET, WHITE, YELLOW
from ytdlplist.utils import ensure_valid_destination


class Playlist:
    """
    Class to store playlist data.

    Attributes
    ----------
    url : str
        Playlist URL.

    id : str
        Playlist ID.

    title : str
        Playlist title.

    json : list[dict[str, str]] | None
        List of JSON objects from the playlist.

    audio_player : Callable[..., Coroutine[Any, Any, None]]
        Coroutine to play a sound file.

    Methods
    -------
    is_valid_plist_url(url: str) -> bool
        Check if a URL is a valid YouTube playlist URL.

    validate_playlists(input_playlists: list[str]) -> list[str]
        Remove duplicate playlists from a list.

    get_title() -> str
        Get the title of a YouTube playlist using yt-dlp.

    get_playlist_id() -> str
        Get the ID of a YouTube playlist from a URL.

    get_json_from_playlist() -> list[dict[str, str]]
        Get a list of JSON objects from a YouTube playlist using yt-dlp.
    """

    def __init__(
        self, url: str, audio_player: Callable[..., Coroutine[Any, Any, None]]
    ) -> None:
        self.url: str = url.strip().replace("//music.youtube.", "//www.youtube.")
        if "&" in self.url:
            self.url = self.url.split("&")[0]
        self.id: str = self.get_playlist_id()
        self.audio_player: Callable[..., Coroutine[Any, Any, None]] = audio_player
        self.json: list[dict[str, str]] | None = None
        try:
            self.json = self.get_json_from_playlist()
        except CalledProcessError:
            pass
        super().__init__()

    async def async_init(self):
        title_task = asyncio.create_task(self.get_title())
        await title_task
        self.title: str = title_task.result()

    async def get_title(self) -> str:
        """
        Get the title of a YouTube playlist using yt-dlp.

        Parameters
        ----------
        playlist_url : str
            YouTube playlist URL or ID.

        Returns
        -------
        str
            Playlist title.

        Raises
        ------
        subprocess.CalledProcessError :
            If an error occurs when running the yt-dlp command.
        """
        if "https" in self.url:
            url = self.url
        else:
            url = f"https://www.youtube.com/playlist?list={self.id}"
        print(f"{YELLOW}Getting playlist title... ", end="", flush=True)
        title: str = (
            subprocess.check_output(
                args=f"yt-dlp {url} --skip-download -I 1:1 --print playlist_title --quiet --no-warnings",
                shell=True,
            )
            .decode()
            .strip()
        )
        print(
            f"{GREEN}Done.",
            "\n",
            f"{YELLOW}Title: {MAGENTA}{title}{RESET}",
            "\n",
            sep="",
            flush=True,
        )
        return title

    def get_playlist_id(self) -> str:
        """
        Get the ID of a YouTube playlist from a URL.

        Returns
        -------
        str
            Playlist ID.

        Raises
        ------
        ValueError :
            If the URL is invalid.
        """
        playlist_id_matches: re.Match[str] | None = re.search(
            pattern=r"list=(?P<id>[a-zA-Z0-9_-]+)", string=self.url
        )
        if (
            not playlist_id_matches
            or not playlist_id_matches.group("id")
            or type(playlist_id_matches.group("id")) is not str
        ):
            raise ValueError("Invalid playlist URL.")
        else:
            playlist_id: str = playlist_id_matches.group("id")
            return playlist_id

    def get_json_from_playlist(self) -> list[dict[str, str]]:
        """
        Get a list of JSON objects from a YouTube playlist using yt-dlp.

        Returns
        -------
        list[dict[str, str]]
            List of JSON objects from the playlist.

        Raises
        ------
        subprocess.CalledProcessError :
            If an error occurs when running the yt-dlp command.
        """
        if "https" in self.url:
            url: str = self.url
        else:
            url = f"https://www.youtube.com/playlist?list={self.id}"
        print(f"  {YELLOW}Downloading playlist information... ", end="", flush=True)
        plist_data: list[str] = []
        plist_data = (
            subprocess.check_output(
                f"yt-dlp -j --flat-playlist {url} --quiet --no-warnings",
                shell=True,
            )
            .decode()
            .split("\n")
        )
        playlist_entries: list[str] = [j.strip() for j in plist_data if j]
        results_json: list[dict[str, Any]] = []
        for entry in playlist_entries:
            try:
                results_json.append(json.loads(entry))
            except json.JSONDecodeError:
                continue
        print(
            f"{GREEN}Done.{RESET}",
            f"  {YELLOW}Found {MAGENTA}{len(results_json)}{YELLOW} tracks.{RESET}",
            "\n",
            sep="",
            end="\n",
            flush=True,
        )
        return results_json

    async def download(
        self,
        audio_only: bool = True,
        output_dir: str = ".",
        output_ext: str = "mp3",
        interval: int = 30,
    ) -> None:
        """
        Download all videos in a YouTube playlist using yt-dlp.

        Parameters
        ----------
        audio_only : bool, optional
            Whether to download only the audio, by default True
        output_dir : str, optional
            Output directory, by default "."
        output_ext : str, optional
            Output file extension, by default "mp3"
        interval : int, optional
            Interval between downloads in seconds, by default 30

        Raises
        ------
        ValueError :
            If the playlist URL is invalid.
        OSError :
            If the output directory does not exist.
        """
        if self.json:
            video_json: list[dict[str, str]] = self.json
        else:
            try:
                video_json = self.get_json_from_playlist()
            except CalledProcessError as e:
                raise ValueError(
                    f"  {YELLOW}[{RED}SKIP{YELLOW}] {RED}Error retrieving playlist information for playlist id {MAGENTA}{self.id}{YELLOW}: {RED}{e}{RESET}"
                )

        results: dict[str, int] = {"success": 0, "error": 0}
        for i, video in enumerate(video_json):
            progress = (
                f"{WHITE}[{DARK}{i+1}{WHITE}/{DARK}{len(video_json)}{WHITE}]{RESET}"
            )
            print(
                f"  {progress} {YELLOW}Downloading {MAGENTA}{video['title']}{YELLOW}... ",
                end=RESET,
                flush=True,
            )

            try:
                _result: int = self.download_track(
                    video_id=video["id"],
                    audio_only=audio_only,
                    output_dir=output_dir,
                    output_ext=output_ext,
                )
                if _result > 0:
                    await self.audio_player("failbeep.wav")
                    results["error"] += 1
                    continue
                else:
                    results["success"] += 1
                    time.sleep(interval)
                    await self.audio_player("successbeep.wav")
                    print(f"{GREEN}Done.{RESET}")
            except subprocess.CalledProcessError as e:
                print(f"{RED}An error occurred:", e, RESET)
                await self.audio_player("failbeep.wav")
                results["error"] += 1
                continue
            except ChildProcessError as e:
                print(f"{RED}An error occurred:", e, RESET)
                await self.audio_player("failbeep.wav")
                results["error"] += 1
                continue
            except OSError as e:
                print(f"{RED}An error occurred:", e, RESET)
                await self.audio_player("failbeep.wav")
                results["error"] += 1
                continue
        await self.audio_player("slidebeep.wav")
        print(
            f"{YELLOW}Downloaded {GREEN}{results['success']} tracks{YELLOW} with {RED}{results['error']} errors.{RESET}"
        )

    @staticmethod
    def download_track(
        video_id: str,
        audio_only: bool = True,
        output_dir: str = ".",
        output_ext: str = "mp3",
    ) -> int:
        """
        Download a single track from YouTube using yt-dlp.

        Parameters
        ----------
        video_id : str
            YouTube video ID.
        audio_only : bool, optional
            Whether to download only the audio, by default True
        output_dir : str, optional
            Output directory, by default "."
        output_ext : str, optional
            Output file extension, by default "mp3"

        Raises
        ------
        OSError :
            If the output directory does not exist.
        ChildProcessError :
            If an error occurs when downloading the video.
        subprocess.CalledProcessError :
            If an error occurs when running the yt-dlp command.
        """
        try:
            ensure_valid_destination(output_dir)
        except OSError as e:
            print(f"{RED}An error occurred:", e, RESET)
            return 1
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Download the video
        _args: list[str] = ["yt-dlp", video_url]
        if audio_only:
            _args.append("--extract-audio")
            _args.append("--audio-format")
            _args.append(output_ext)
        else:
            _args.append("--format")
            _args.append(output_ext)
        _args.append("--output")
        _args.append(f"{output_dir}/%(title)s.%(ext)s")
        _args.append("--quiet")
        _args.append("--no-warnings")
        try:
            result: subprocess.CompletedProcess[bytes] = subprocess.run(
                args=_args, capture_output=True
            )
            if result.stderr:
                print(f"{RED}Error downloading video.", result.stderr.decode())
                return 1
            else:
                return 0
        except subprocess.CalledProcessError as e:
            raise ChildProcessError("Error downloading video:", e, e.__traceback__)

    @staticmethod
    def is_valid_plist_url(url: str) -> bool:
        """
        Check if a URL is a valid YouTube playlist URL.

        Parameters
        ----------
        url : str
            URL to check.

        Returns
        -------
        bool
            Whether the URL is a valid YouTube playlist URL.
        """
        return all([url and "https://" in url and "?list=" in url])

    @staticmethod
    def validate_playlists(input_playlists: list[str]) -> list[str]:
        """
        Remove duplicate playlists from a list.

        Parameters
        ----------
        playlists : list[str]
            List of playlists.

        Returns
        -------
        list[str]
            List of playlists with duplicates removed.
        """
        playlists: list[str] = []
        for playlist in input_playlists:
            if Playlist.is_valid_plist_url(playlist) and playlist not in playlists:
                playlists.append(playlist)
        return playlists
