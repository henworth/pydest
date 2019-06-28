import aiohttp
import re
import json

from functools import partial

from .base import _BaseAPI
from .group import Group
from .user import User



class API(_BaseAPI):
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

        self.group = Group(session, client_id, client_secret)
        self.user = User(session, client_id, client_secret)

    async def get_destiny_manifest(self):
        """Returns the current version of the manifest

        Returns:
            json (dict)
        """
        url = f'{self.DESTINY2_URL}/Manifest'
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
        url = f'{self.DESTINY2_URL}/Armory/Search/{entity_type}/{search_term}/'
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
        url = f'{self.DESTINY2_URL}/SearchDestinyPlayer/{membership_type}/{display_name}/'
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
        url = f'{self.DESTINY2_URL}/{membership_type}/Profile/{membership_id}/'
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
        url = f'{self.DESTINY2_URL}/{membership_type}/Profile/{membership_id}/Character/{character_id}/'
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
        url = f'{self.DESTINY2_URL}/Clan/{group_id}/WeeklyRewardState/'
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
        url = f'{self.DESTINY2_URL}/{membership_type}/Profile/{membership_id}/Item/{item_instance_id}/'
        return await self._get_request(url, params)

    async def get_post_game_carnage_report(self, activity_id):
        """Gets the available post game carnage report for the activity ID

        Args:
            activity_id (int):
                The ID of the activity whose PGCR is requested

        Returns:
            json (dict)
        """
        url = f'{self.DESTINY2_URL}/Stats/PostGameCarnageReport/{activity_id}/'
        return await self._get_request(url)

    async def get_historical_stats_definition(self):
        """Gets historical stats definitions

        Returns:
            json (dict)
        """
        url = f'{self.DESTINY2_URL}/Stats/Definition/'
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
        url = f'{self.DESTINY2_URL}/{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/'
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
        url = f'{self.DESTINY2_URL}/{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/Activities/'
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
        url = f'{self.DESTINY2_URL}/Milestones/{milestone_hash}/Content/'
        return await self._get_request(url)

    async def get_public_milestones(self):
        """Gets information about the current public Milestones

        Returns:
            json (dict)
        """
        url = f'{self.DESTINY2_URL}/Milestones/'
        return await self._get_request(url)

    async def get_milestone_definitions(self, milestone_hash):
        """Gets the milestone definition for a given milestone hash

        Args:
            milestone_hash (int):
                The hash value that represents the milestone within the manifest

        Returns:
            json(dict)
        """
        url = f'{self.DESTINY2_URL}/Manifest/DestinyMilestoneDefinition/{milestone_hash}/'
        return await self._get_request(url)

    async def get_group(self, group_id):
        return await self.group.get_by_id(group_id)

    async def get_group_members(self, group_id):
        return await self.group.get_group_members(group_id)

    async def get_group_pending_members(self, group_id, access_token):
        return await self.group.get_group_pending_members(group_id, access_token)
