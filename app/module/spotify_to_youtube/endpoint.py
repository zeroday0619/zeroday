import asyncio
from asyncio.futures import Future

from typing import Union, Optional, List
from async_spotify import SpotifyApiClient
from spotify_uri.search import Search
from spotify_uri.local import Local
from spotify_uri.playlist import Playlist
from spotify_uri.user import User
from spotify_uri.artist import Artist
from spotify_uri.album import Album
from spotify_uri.track import Track
from spotify_uri.episode import Episode
from app.controller.logger import Logger


class SpotifyEndpoint:
    def __init__(
        self, 
        source: Union[Search, Local, Playlist, User, Artist, Album, Track, Episode], 
        api_client: Optional[SpotifyApiClient], 
        loop: Optional[asyncio.AbstractEventLoop] = None    
    ):
        self.fut: Optional[Future[List]] = None
        self.loop = loop or asyncio.get_event_loop()
        self.api_client = api_client
        self.type = source.type
        self.id = source.id

    @Logger.set()
    async def router(self):
        if self.type == "search":
            await self.api_client.close_client()
            raise TypeError(self.type)
        if self.type == "local":
            return None
        if self.type == "playlist":
            agx = await self.parse_playlist_info()
            return agx
        if self.type == "user":
            return None
        if self.type == "artist":
            return None
        if self.type == "album":
            return None
        if self.type == "track":
            return None
        if self.type == "episode":
            return None
        return NotImplementedError

    @Logger.set()
    async def parse_playlist_info(self):
        source: dict = await self.api_client.playlists.get_tracks(self.id)
        result = [
            [
                index["track"]["name"] for index in source["items"]
            ],
            [
                [
                    [
                        ac["name"] for ac in index["track"]["artists"]
                    ][ix] for ix in range(len(
                        [
                            ac["name"] for ac in index["track"]["artists"]
                        ]
                    ))
                ] for index in source["items"]
            ]
        ]
        # Logger.generate_log().debug(msg=result)
        # self.fut = asyncio.gather(self.stop_all(), *result, return_exceptions=True)
        # self.loop.run_until_complete(self.fut)
        # res = self.fut.result()
        await self.api_client.close_client()
        # self.loop.close()
        # Logger.generate_log().debug(msg=res)
        return result