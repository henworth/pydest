import aiohttp
import re
import json
import urllib
from functools import partial

import pydest


PLATFORM_URL = 'https://www.bungie.net/Platform'
DESTINY2_URL = f'{PLATFORM_URL}/Destiny2'
APP_URL = f'{PLATFORM_URL}/App'
USER_URL = f'{PLATFORM_URL}/User'
CONTENT_URL = f'{PLATFORM_URL}/Content'
GROUP_URL = f'{PLATFORM_URL}/GroupV2'

GROUP_FILTER_NONE = 0
GROUP_TYPE_CLAN = 1


class API:
    """This module contains async requests for the Destiny 2 API.
    There is some documentation provided here as to how to use
    these functions, but you will likely need to refer to the
    official API documentation as well. The documentation can be
    found at https://bungie-net.github.io/multi/index.html
    """

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
        except aiohttp.ClientResponseError:
            raise pydest.PydestException("Could not connect to Bungie.net")
        return json_res

    async def _get_request(self, url, params=None, access_token=None):
        """Make an async GET request and attempt to return json (dict)"""
        return await self._request('GET', url, access_token=access_token, params=params)

    async def _post_request(self, url, data=None, access_token=None):
        """Make an async POST request and attempt to return json (dict)"""
        return await self._request('POST', url, access_token=access_token, data=data)

    async def refresh_oauth_token(self, refresh_token):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        try:
            async with self.session.post(f'{APP_URL}/oauth/token/', headers=None, data=data) as r:
                json_res = await r.json()
        except aiohttp.ClientResponseError:
            raise pydest.PydestException("Could not connect to Bungie.net")
        return json_res

    async def get_bungie_net_user_by_id(self, membership_id):
        """Loads a bungienet user by membership id

        Args:
            membership_id: The requested Bungie.net membership id

        Returns:
            json (dict)
        """
        url = f'{USER_URL}/GetBungieNetUserById/{membership_id}/'
        return await self._get_request(url)

    async def get_membership_data_by_id(self, membership_id, membership_type=-1):
        """Returns a list of accounts associated with the supplied membership ID and membership
        type. This will include all linked accounts (even when hidden) if supplied credentials
        permit it.

        Args:
            membership_id (int):
                The requested Bungie.net membership id
            membership_type (int) [optional]:
                Type of the supplied membership ID. If not provided, data will be returned for all
                applicable platforms.

        Returns:
            json (dict)
        """
        url = f'{USER_URL}/GetMembershipsById/{membership_id}/{membership_type}/'
        return await self._get_request(url)

    async def get_destiny_manifest(self):
        """Returns the current version of the manifest

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/Manifest'
        return await self._get_request(url)

    async def search_destiny_entities(self, entity_type, search_term, page=0):
        """Gets a page list of Destiny items

        Args:
            entity_type (str):
                The type of entity - ex. 'DestinyInventoryItemDefinition'
            search_term (str):
                The full gamertag or PSN id of the player. Spaces and case are ignored
            page (int) [optional]:
                Page number to return

        Returns:
            json (dict)
        """
        params = {'page': page}
        url = f'{DESTINY2_URL}/Armory/Search/{entity_type}/{search_term}/'
        return await self._get_request(url, params)

    async def search_destiny_player(self, membership_type, display_name):
        """Returns a list of Destiny memberships given a full Gamertag or PSN ID

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            display_name (str):
                The full gamertag or PSN id of the player. Spaces and case are ignored.

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/SearchDestinyPlayer/{membership_type}/{display_name}/'
        return await self._get_request(url)

    async def get_profile(self, membership_type, membership_id, components):
        """Returns Destiny Profile information for the supplied membership

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            components (list):
                A list containing the components  to include in the response.
                (see Destiny.Responses.DestinyProfileResponse). At least one
                component is required to receive results. Can use either ints
                or strings.

        Returns:
            json (dict)
        """
        params = {'components': ','.join([str(i) for i in components])}
        url = f'{DESTINY2_URL}/{membership_type}/Profile/{membership_id}/'
        return await self._get_request(url, params)

    async def get_character(self, membership_type, membership_id, character_id, components):
        """Returns character information for the supplied character

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            character_id (int):
                ID of the character
            components (list):
                A list containing the components  to include in the response.
                (see Destiny.Responses.DestinyProfileResponse). At least one
                component is required to receive results. Can use either ints
                or strings.

        Returns:
            json (dict)
        """
        params = {'components': ','.join([str(i) for i in components])}
        url = f'{DESTINY2_URL}/{membership_type}/Profile/{membership_id}/Character/{character_id}/'
        return await self._get_request(url, params)

    async def get_clan_weekly_reward_state(self, group_id):
        """
        Verb: GET
        Path: /Clan/{groupId}/WeeklyRewardState/

        Returns information on the weekly clan rewards and if the clan has earned
        them or not. Note that this will always report rewards as not redeemed.

        Args:
            group_id (int):
                A valid group ID of a clan

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/Clan/{group_id}/WeeklyRewardState/'
        return await self._get_request(url)

    async def get_item(self, membership_type, membership_id, item_instance_id, components):
        """Retrieve the details of an instanced Destiny Item. An instanced Destiny
        item is one with an ItemInstanceId. Non-instanced items, such as materials,
        have no useful instance-specific details and thus are not queryable here.

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            item_instance_id (int):
                The instance ID of the item
            components (list):
                A list containing the components to include in the response
                (see Destiny.Responses.DestinyItemResponse). At least one
                component is required to receive results. Can use either ints
                or strings.

        Returns:
            json (dict)
        """
        params = {'components': ','.join([str(i) for i in components])}
        url = f'{DESTINY2_URL}/{membership_type}/Profile/{membership_id}/Item/{item_instance_id}/'
        return await self._get_request(url, params)

    async def get_post_game_carnage_report(self, activity_id):
        """Gets the available post game carnage report for the activity ID

        Args:
            activity_id (int):
                The ID of the activity whose PGCR is requested

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/Stats/PostGameCarnageReport/{activity_id}/'
        return await self._get_request(url)

    async def get_historical_stats_definition(self):
        """Gets historical stats definitions

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/Stats/Definition/'
        return await self._get_request(url)

    async def get_historical_stats(self, membership_type, membership_id, character_id=0, groups=[], modes=[]):
        """Gets historical stats for indicated character

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            character_id (int) [optional]:
                The id of the character to retrieve stats for. If not provided, stats for all
                characters will be retrieved.
            groups (list - str/int):
                A list containing the groups of stats to include in the response
                (see Destiny.HistoricalStats.Definitions.DestinyStatsGroupType).
            modes (list - str/int):
                A list containing the game modes to include in the response
                (see Destiny.HistoricalStats.Definitions.DestinyActivityModeType).

        Returns:
            json (dict)
        """
        params = {'groups': ','.join([str(i) for i in groups]), 'modes': ','.join([
            str(i) for i in modes])}
        url = f'{DESTINY2_URL}/{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/'
        return await self._get_request(url, params)

    async def get_activity_history(self, membership_type, membership_id, character_id=0, mode=0, count=10):
        """Gets activity history for indicated character
        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            character_id (int) [optional]:
                The id of the character to retrieve stats for. If not provided, stats for all
                characters will be retrieved.
            mode (int) [optional]:
                The id of the game mode to include in the response
                (see Destiny.HistoricalStats.Definitions.DestinyActivityModeType).
            count (int) [optional]:
                Limit to returned results.

        Returns:
            json (dict)
        """
        params = {'count': count, 'mode': mode}
        url = f'{DESTINY2_URL}/{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/Activities/'
        return await self._get_request(url, params)

    async def get_public_milestone_content(self, milestone_hash):
        """Gets custom localized content for the milestone of
        the given hash, if it exists.

        Args:
            milestone_hash (int):
                A valid hash id of a Destiny 2 milestone

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/Milestones/{milestone_hash}/Content/'
        return await self._get_request(url)

    async def get_public_milestones(self):
        """Gets information about the current public Milestones

        Returns:
            json (dict)
        """
        url = f'{DESTINY2_URL}/Milestones/'
        return await self._get_request(url)

    async def get_group(self, group_id):
        """Get information about a specific group

        Path: /GroupV2/{group_id}/
        Verb: GET

        Args:
            group_id (int):
                The id of the group

        Returns:
            json (dict)
        """
        url = f'{GROUP_URL}/{group_id}/'
        return await self._get_request(url)

    async def get_groups_for_member(self, membership_type, membership_id):
        """Gets information about the groups an individual member has joined

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id

        Returns:
            json (dict)
        """
        url = f'{GROUP_URL}/User/{membership_type}/{membership_id}/{GROUP_FILTER_NONE}/{GROUP_TYPE_CLAN}/'
        return await self._get_request(url)

    async def get_group_members(self, group_id):
        """Gets list of members in a group

        Args:
            group_id (int):
                The id of the group

        Returns:
            json (dict)
        """
        url = f'{GROUP_URL}/{group_id}/Members/'
        return await self._get_request(url)

    async def get_group_pending_members(self, group_id, access_token):
        """Gets list of pending members in a group

        Path: /GroupV2/{group_id}/Members/Pending/
        Verb: GET

        Required Scope(s):
            oauth2: AdminGroups

        Args:
            group_id (int):
                The id of the group
            access_token (str):
                OAuth access token

        Returns:
            json(dict)
        """
        url = f'{GROUP_URL}/{group_id}/Members/Pending/'
        return await self._get_request(url, access_token=access_token)

    async def get_group_invited_members(self, group_id, access_token):
        """Gets list of invited members in a group

        Path: /GroupV2/{group_id}/Members/InvitedIndividuals/
        Verb: GET

        Args:
            group_id (int):
                The id of the group
            access_token (str):
                OAuth access token

        Returns:
            json(dict)
        """
        url = f'{GROUP_URL}/{group_id}/Members/InvitedIndividuals/'
        return await self._get_request(url, access_token=access_token)

    async def group_invite_member(self, group_id, membership_type, membership_id, message, access_token):
        """Invite a user to join this group

        Path: /GroupV2/{group_id}/Members/IndividualInvite/{membership_type}/{membership_id}/
        Verb: POST

        Required Scope(s):
            oauth2: AdminGroups

        Args:
            group_id (int):
                The id of the group
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            message (str):
                Message to send along with the invite
            access_token (str):
                OAuth access token

        Returns:
            json(dict)
        """
        data = {'message': message}
        url = f'{GROUP_URL}/{group_id}/Members/IndividualInvite/{membership_type}/{membership_id}/'
        return await self._post_request(url, data=data, access_token=access_token)

    async def group_kick_member(self, group_id, membership_type, membership_id, access_token):
        """Kick a user from this group

        Path: /GroupV2/{group_id}/Members/{membership_type}/{membership_id}/Kick/
        Verb: POST

        Required Scope(s):
            oauth2: AdminGroups

        Args:
            group_id (int):
                The id of the group
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            access_token (str):
                OAuth access token

        Returns:
            json(dict)
        """
        url = f'{GROUP_URL}/{group_id}/Members/{membership_type}/{membership_id}/Kick/'
        return await self._post_request(url, access_token=access_token)

    async def group_approve_pending_member(self, group_id, membership_type, membership_id, message, access_token):
        """Approve a pending a user applying to join this group

        Path: /GroupV2/{group_id}/Members/Approve/{membership_type}/{membership_id}/
        Verb: POST

        Required Scope(s):
            oauth2: AdminGroups

        Args:
            group_id (int):
                The id of the group
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                The requested Bungie.net membership id
            message (str):
                Message to send along with the invite
            access_token (str):
                OAuth access token

        Returns:
            json(dict)
        """
        data = {'message': message}
        url = f'{GROUP_URL}/{group_id}/Members/Approve/{membership_type}/{membership_id}/'
        return await self._post_request(url, data=data, access_token=access_token)

    async def get_milestone_definitions(self, milestone_hash):
        """Gets the milestone definition for a given milestone hash

        Args:
            milestone_hash (int):
                The hash value that represents the milestone within the manifest

        Returns:
            json(dict)
        """
        url = f'{DESTINY2_URL}/Manifest/DestinyMilestoneDefinition/{milestone_hash}/'
        return await self._get_request(url)
