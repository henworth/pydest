import aiohttp
import asyncio

from pydest.api import API
from pydest.base import _BaseAPI
from pydest.errors import PydestException, PydestTokenException
from pydest.manifest import Manifest


class Pydest(_BaseAPI):

    def __init__(self, api_key, loop=None, client_id=None, client_secret=None):
        """Base class for Pydest

        Args:
            api_key (str):
                Bungie.net API key
            loop [optional]:
                AsyncIO event loop, if not passed one will be created
            client_id (str) [optional]:
                Bungie.net application client id
            client_secret (str) [optional]:
                Bungie.net application client id
        """
        headers = {'X-API-KEY': api_key}

        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self._loop, headers=headers)

        super(Pydest, self).__init__(self._session, client_id, client_secret)

        self.api = API(self._session, client_id, client_secret)
        self._manifest = Manifest(self.api)

    async def refresh_oauth_token(self, refresh_token):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        try:
            async with self._session.post(f'{self.APP_URL}/oauth/token/', headers=None, data=data) as r:
                json_res = await r.json()
        except aiohttp.ClientResponseError:
            raise PydestException("Could not connect to Bungie.net")
        return json_res

    async def decode_hash(self, hash_id, definition, language='en'):
        """Get the corresponding static info for an item given it's hash value from the Manifest

        Args:
            hash_id (str):
                The unique identifier of the entity to decode
            definition (str):
                The type of entity to be decoded (ex. 'DestinyClassDefinition')
            language (str):
                The language to use when retrieving results from the Manifest

        Returns:
            json (dict)

        Raises:
            PydestException
        """
        return await self._manifest.decode_hash(hash_id, definition, language)

    async def update_manifest(self, language='en'):
        """Update the manifest if there is a newer version available

        Args:
            language (str) [optional]:
                The language corresponding to the manifest to update
        """
        await self._manifest.update_manifest(language)

    def close(self):
        asyncio.ensure_future(self._session.close())
