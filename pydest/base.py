import aiohttp
import logging
import urllib

from pydest.errors import PydestException, PydestTokenException

logging.getLogger(__name__)


class _BaseAPI(object):

    PLATFORM_URL = 'https://www.bungie.net/Platform'
    DESTINY2_URL = f'{PLATFORM_URL}/Destiny2'
    APP_URL = f'{PLATFORM_URL}/App'
    USER_URL = f'{PLATFORM_URL}/User'
    CONTENT_URL = f'{PLATFORM_URL}/Content'
    GROUP_URL = f'{PLATFORM_URL}/GroupV2'

    GROUP_FILTER_NONE = 0
    GROUP_TYPE_GENERAL = 0
    GROUP_TYPE_CLAN = 1

    def __init__(self, session, client_id=None, client_secret=None):
        self.session = session
        self.client_id = client_id
        self.client_secret = client_secret

    async def _request(self, req_type, url, access_token=None, params=None, data=None):
        """Make an async HTTP request and attempt to return json (dict)"""
        headers = {}
        if access_token:
            headers.update({'Authorization': f"Bearer {access_token}"})
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self.session.request(req_type, encoded_url, headers=headers, params=params, json=data) as r:
                if r.status == 401:
                    raise pydest.PydestTokenException(
                        "Access token has expired, refresh needed")
                else:
                    json_res = await r.json()
        except aiohttp.ContentTypeError:
            raise PydestException(f"Could not decode json from response: {await r.text()}")
        except aiohttp.ClientResponseError:
            raise PydestException(f"Could not connect to Bungie.net: {await r.text()}")
        return json_res

    async def _get_request(self, url, params=None, access_token=None):
        """Make an async GET request and attempt to return json (dict)"""
        return await self._request('GET', url, access_token=access_token, params=params)

    async def _post_request(self, url, data=None, access_token=None):
        """Make an async POST request and attempt to return json (dict)"""
        return await self._request('POST', url, access_token=access_token, data=data)
