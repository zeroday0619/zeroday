import spotify_uri

from typing import Optional
from app.controller.logger import Logger  # Logger
from app.controller import spotify_credentials  # Load Spotify credentials

# Spotify api wrapper
from async_spotify import SpotifyApiClient
from async_spotify.authentification.authorization_flows import ClientCredentialsFlow
from .endpoint import SpotifyEndpoint


class SpotifyConverter:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> None:
        """Spotify Extension | Spotify to Youtube

        :param client_id: [Optional] : developer.spotify.com 에서 얻은 client id
        :param client_secret: [Optional] : developer.spotify.com 에서 얻은 client secret
        """
        self.client_id: Optional[str] = client_id or spotify_credentials.get("client_id")
        self.client_secret: Optional[str] = client_secret or spotify_credentials.get("client_secret")

    def __repr__(self) -> str:
        if (self.client_id is None or self.client_secret is None) or (self.client_id == "" or self.client_secret == ""):
            raise NotImplementedError("client_id or client_secret is missing.")
        else:
            return ""

    def auth_flow(self) -> ClientCredentialsFlow:
        return ClientCredentialsFlow(
            application_id=self.client_id,
            application_secret=self.client_secret
        )

    async def get_api_client(self) -> SpotifyApiClient:
        auth_flow = self.auth_flow()
        api_client = SpotifyApiClient(authorization_flow=auth_flow)
        await api_client.get_auth_token_with_client_credentials()
        await api_client.create_new_client()
        return api_client

    @Logger.set()
    async def get_playlist_info(self, uri: str):
        api_client = await self.get_api_client()
        source = spotify_uri.parse(uri=uri)
        end = SpotifyEndpoint(source=source, api_client=api_client)
        resp = await end.router()
        name, artist = resp[0], resp[1]
        n_name = len(name)

        if n_name == len(artist):
            result = [{"name": f"{name[n]} - {', '.join(artist[n])}"} for n in range(n_name)]
            return {"status": True, "data": result}
        else:
            return {"status": False, "data": None}

