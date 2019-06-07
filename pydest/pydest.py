import aiohttp
import asyncio
import os
import zipfile

from pydest.api import API
from pydest.manifest import Manifest


class Pydest:

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
        self.api = API(self._session, client_id, client_secret)
        self._manifest = Manifest(self.api)

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

    async def close(self):
        await self._session.close()


class PydestException(Exception):
    pass


class PydestTokenException(PydestException):
    pass
