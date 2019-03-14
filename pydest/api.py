import aiohttp
import urllib

import pydest

DESTINY2_URL = 'https://www.bungie.net/Platform'
APP_URL = f"{DESTINY2_URL}/App"
USER_URL = f'{DESTINY2_URL}/User'
CONTENT_URL = f"{DESTINY2_URL}/Content"
GROUP_URL = 'https://www.bungie.net/Platform/GroupV2/'


class API:
    """This module contains async requests for the Destiny 2 API.
    There is some documentation provided here as to how to use
    these functions, but you will likely need to refer to the
    official API documentation as well. The documentation can be
    found at https://bungie-net.github.io/multi/index.html


    App Endpoints
        App.GetApplicationApiUsage
            - /App/ApiUsage/{applicationId}/
        App.GetBungieApplications
            - /App/FirstParty/

    User Endpoints
        GET: /User/GetBungieNetUserById/{id}/
        GET: /User/GetAvailableThemes/
        GET: /User/GetMembershipsById/{membershipId}/{membershipType}/
        GET: /User/GetMembershipsForCurrentUser/
        GET: /User/{membershipId}/Partnerships/

    Content Endpoints
        GET: /Content/GetContentType/{type}/
        GET: /Content/GetContentById/{id}/{locale}/
        GET: /Content/GetContentByTagAndType/{tag}/{type}/{locale}/
        GET: /Content/Search/{locale}/
        GET: /Content/SearchContentByTagAndType/{tag}/{type}/{locale}/



    """

    def __init__(self, api_key, session, locale):
        self.api_key = api_key
        self.session = session
        self.locale = locale

    async def _get_request(self, url, params=None, token=None):
        """Make an async GET request and attempt to return json (dict)"""
        headers = {'X-API-KEY': self.api_key}
        if token:
            headers.update({'Authorization': f"Bearer {token}"})
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self.session.get(encoded_url, headers=headers, params=params) as r:
                json_res = await r.json()
        except aiohttp.ClientResponseError:
            raise pydest.PydestException("Could not connect to Bungie.net")
        return json_res

    async def get_application_api_usage(self, applicationId, oauth2Token):
        """
        Verb: GET
        Path: /App/ApiUsage/{applicationId}/
        Get API usage by application for time frame specified.
        You can go as far back as 30 days ago, and can ask for up to a 48 hour window of time in a single request.
        You must be authenticated with at least the ReadUserData permission to access this endpoint.

        Required Scope(s)
            oauth2: ReadUserData

        Args:
            applicationId (int): ID of the application to get usage statistics.
            oauth2Token (str): token Bearer oauth2

        Returns:
            json (dict)
        """
        url = f"{APP_URL}/ApiUsage/{applicationId}"
        return await self._get_request(url, token=oauth2Token)

    async def get_bungie_application(self):
        """
        Verb: GET

        Path: /App/FirstParty/

        Get list of applications created by Bungie.

        Returns:
            json (dict)
        """
        url = f"{APP_URL}/App/FirstParty"
        return await self._get_request(url)

    async def get_bungie_net_user_by_id(self, bungie_id):
        """
        Verb: GET

        Path: /User/GetBungieNetUserById/{id}/

        Loads a bungienet user by membership id.

        Args:
            bungie_id {int} -- The requested Bungie.net membership id.

        Returns:
            json (dict)
        """
        url = USER_URL + f'GetBungieNetUserById/{bungie_id}/'
        return await self._get_request(url)

    async def search_users_by_name(self, name):
        """
        Verb: GET

        Path: /User/SearchUsers/

        Returns a list of possible users based on the search string

        Args:
            name (str): The search string.
        """
        url = f"{USER_URL}/SearchUsers/?q={name}"
        return await self._get_request(url)

    async def get_avaliable_themes(self):
        """
        Verb: GET

        Path: /User/GetAvailableThemes/

        Returns a list of all available user themes.

        Returns:
                json (dict)

        """
        url = f"{USER_URL}/GetAvailableThemes"
        return await self._get_request(url)

    async def get_membership_data_by_id(self, bungie_id, membership_type=-1):
        """
        Verb: GET

        Path: /User/GetMembershipsById/{membershipId}/{membershipType}/

        Returns a list of accounts associated with the supplied membership ID and membership
        type. This will include all linked accounts (even when hidden) if supplied credentials
        permit it.

        Args:
            bungie_id:
                The requested Bungie.net membership id
            membership_type (optional):
                Type of the supplied membership ID. If not provided, data will be returned for all
                applicable platforms.

        Returns:
            json (dict)
        """
        url = USER_URL + f'GetMembershipsById/{bungie_id}/{membership_type}/'
        return await self._get_request(url)

    async def get_linked_profiles(self, bungie_id, membership_type=-1):
        """Returns a summary information about all profiles linked to the requesting membership
        type/membership ID that have valid Destiny information. The passed-in Membership
        Type/Membership ID may be a Bungie.Net membership or a Destiny membership. It only returns
        the minimal amount of data to begin making more substantive requests, but will hopefully 
        serve as a useful alternative to UserServices for people who just care about Destiny data.
        Note that it will only return linked accounts whose linkages you are allowed to view.

        Args:
            bungie_id:
                The requested Bungie.net membership id
            membership_type (optional):
                Type of the supplied membership ID. If not provided, data will be returned for all
                applicable platforms.

        Returns:
            json (dict)
        """
        url = USER_URL + f'{membership_type}/Profile/{bungie_id}/LinkedProfiles/'
        return await self._get_request(url)

    async def get_membership_data_for_current_user(self, oauth2Token):
        """
        Verb: GET

        Path: /User/GetMembershipsForCurrentUser/


        Returns a list of accounts associated with signed in user. 
        This is useful for OAuth implementations that do not give you access to the token response.

        Args:
            oauth2Token (str): token Bearer oauth2
        Returns:
                json (dict)
        """
        url = f"{USER_URL}/GetMembershipsForCurrentUser"
        return await self._get_request(url, oauth2Token)

    async def get_partnerships(self, membershipId):
        """
        Verb: GET

        Path: /User/{membershipId}/Partnerships/

        Returns a user's linked Partnerships.

        Args:
            membershipId (str): The ID of the member for whom partnerships should be returned.
        Returns:
                json (dict)
        """
        url = f"{USER_URL}/{membershipId}/Partnerships"
        return await self._get_request(url)

    async def get_content_type(self, ctype):
        """
        Verb: GET

        Path: /Content/GetContentType/{type}/

        Gets an object describing a particular variant of content.

        Args:
            ctype (str): Content type tag: Help, News, etc. Supply multiple ctypes separated by space.
        Returns:
                json (dict)
        """
        url = f"{CONTENT_URL}/GetContentType/{ctype}/"
        return await self._get_request(url)

    async def get_content_by_id(self, cid, locale=None):
        """
        Verb: GET

        Path: /Content/GetContentById/{id}/{locale}/

        Returns a content item referenced by id
        More -> https://bungie-net.github.io/#Content.GetContentById
        Args:
            ctype (str): Content type tag: Help, News, etc. Supply multiple ctypes separated by space.
            locale (str): the locale
        Returns:
                json (dict)
        """
        if not locale:
            locale = self.locale
        url = f"{CONTENT_URL}/GetContentById/{cid}/{locale}/"
        return await self._get_request(url)

    async def get_content_by_tag_and_type(self, tag, ctype, locale=None):
        """
        Verb: GET

        Path: /Content/GetContentByTagAndType/{tag}/{type}/{locale}/

        Returns the newest item that matches a given tag and Content Type.
        More -> https://bungie-net.github.io/#Content.GetContentByTagAndType
        Args:
            tag (str): Tag used on the content to be searched.
            ctype (str): Content type tag: Help, News, etc. Supply multiple ctypes separated by space.
            locale (str): the locale
        Returns:
                json (dict)
        """
        if not locale:
            locale = self.locale
        url = f"{CONTENT_URL}/GetContentByTagAndType/{tag}/{ctype}/{locale}/"
        return await self._get_request(url)

    async def search_content_with_text(self,searchtext,locale=None,ctype=None,currentpage=None,source=None,tag=None):
        """
        Verb: GET

        Path: /Content/Search/{locale}/

        Gets content based on querystring information passed in. 
        Provides basic search and text search capabilities.. regex ?
        More -> https://bungie-net.github.io/#Content.SearchContentWithText
        Args:
            locale (str): the locale
            ctype (str): Content type tag: Help, News, etc. Supply multiple ctypes separated by space.
            currentpage (int): Page number for the search results, starting with page 1.
            searchtext (str):  Word or phrase for the search.
            source (str): For analytics, hint at the part of the app that triggered the search. Optional.
            tag (str): Tag used on the content to be searched.
        Returns:
                json (dict)
        """

        querystring = {"searchtext":searchtext}

        if ctype:
            querystring.update({"ctype":ctype})
        if currentpage:
            querystring.update({"currentpage":currentpage})
        if source:
            querystring.update({"source":source})
        if tag:
            querystring.update({"tag":tag})


        if not locale:
            locale = self.locale

        url = f"{CONTENT_URL}/Search/{locale}/"
        return await self._get_request(url,params=querystring)


    async def search_content_by_tag_and_type(self, tag, ctype, locale=None,currentpage=None):
        """
        Verb: GET

        Path: /Content/GetContentByTagAndType/{tag}/{type}/{locale}/

        Searches for Content Items that match the given Tag and Content Type.
        More -> https://bungie-net.github.io/#Content.SearchContentByTagAndType
        Args:
            tag (str): Tag used on the content to be searched.
            ctype (str): Content type tag: Help, News, etc. Supply multiple ctypes separated by space.
            locale (str): the locale
        Returns:
                json (dict)
        """
        if not locale:
            locale = self.locale
        querryString=None
        if currentpage:
            querryString={"currentpage":currentpage}
        url = f"{CONTENT_URL}/GetContentByTagAndType/{tag}/{ctype}/{locale}/"
        return await self._get_request(url,params=querryString)


   


    async def get_destiny_manifest(self):
        """Returns the current version of the manifest

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + 'Manifest'
        return await self._get_request(url)
    
    
    async def get_manifest_object(self, entity_type, hash_id):
        """Returns the static definition of an entity of the given Type and hash identifier.
        Examine the API Documentation for the Type Names of entities that have their own definitions.
        Note that the return type will always *inherit from* DestinyDefinition, but the specific type
        returned will be the requested entity type if it can be found. Please don't use this as a chatty
        alternative to the Manifest database if you require large sets of data, but for simple and one-off
        accesses this should be handy.

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + f'Manifest/{entity_type}/{hash_id}/'
        return await self._get_request(url)

    async def search_destiny_entities(self, entity_type, search_term, page=0):
        """Gets a page list of Destiny items

        Args:
            entity_type:
                The type of entity - ex. 'DestinyInventoryItemDefinition'
            search_term:
                The full gamertag or PSN id of the player. Spaces and case are ignored
            page (optional):
                Page number to return

        Returns:
            json (dict)
        """
        payload = {'page': page}
        url = DESTINY2_URL + f'Armory/Search/{entity_type}/{search_term}/'
        return await self._get_request(url, payload)

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
        url = DESTINY2_URL + f'SearchDestinyPlayer/{membership_type}/{display_name}/'
        return await self._get_request(url)

    async def get_profile(self, membership_type, membership_id, components):
        """Returns Destiny Profile information for the supplied membership

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
            components (list):
                A list containing the components  to include in the response.
                (see Destiny.Responses.DestinyProfileResponse). At least one
                component is required to receive results. Can use either ints
                or strings.

        Returns:
            json (dict)
        """
        payload = {'components': ','.join([str(i) for i in components])}
        url = DESTINY2_URL + f'{membership_type}/Profile/{membership_id}/'
        return await self._get_request(url, payload)

    async def get_character(self, membership_type, membership_id, character_id, components):
        """Returns character information for the supplied character

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
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
        payload = {'components': ','.join([str(i) for i in components])}
        url = DESTINY2_URL + f'{membership_type}/Profile/{membership_id}/Character/{character_id}/'
        return await self._get_request(url, payload)

    async def get_clan_weekly_reward_state(self, group_id):
        """Returns information on the weekly clan rewards and if the clan has earned
        them or not. Note that this will always report rewards as not redeemed.

        Args:
            group_id (int):
                A valid group ID of a clan

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + f'Clan/{group_id}/WeeklyRewardState/'
        return await self._get_request(url)

    async def get_item(self, membership_type, membership_id, item_instance_id, components):
        """Retrieve the details of an instanced Destiny Item. An instanced Destiny
        item is one with an ItemInstanceId. Non-instanced items, such as materials,
        have no useful instance-specific details and thus are not queryable here.

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
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
        payload = {'components': ','.join([str(i) for i in components])}
        url = DESTINY2_URL + f'{membership_type}/Profile/{membership_id}/Item/{item_instance_id}/'
        return await self._get_request(url, payload)

    async def get_post_game_carnage_report(self, activity_id):
        """Gets the available post game carnage report for the activity ID

        Args:
            activity_id (int):
                The ID of the activity whose PGCR is requested

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + f'Stats/PostGameCarnageReport/{activity_id}/'
        return await self._get_request(url)

    async def get_historical_stats_definition(self):
        """Gets historical stats definitions

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + 'Stats/Definition/'
        return await self._get_request(url)

    async def get_historical_stats(self, membership_type, membership_id, character_id=0, groups=[], modes=[]):
        """Gets historical stats for indicated character

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
            character_id (int) [optional]:
                The id of the character to retrieve stats for. If not provided, stats for all
                characters will be retrieved.
            groups (list - str/int):
                A list containing the groups of stats to include in the response
                (see Destiny.HistoricalStats.Definitions.DestinyStatsGroupType).
            modes (list - str/int):
                A list containing the game modes to include in the response
                (see Destiny.HistoricalStats.Definitions.DestinyActivityModeType).

        """
        payload = {'groups': ','.join([str(i) for i in groups]), 'modes': ','.join([str(i) for i in modes])}
        url = DESTINY2_URL + f'{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/'
        return await self._get_request(url, payload)

    async def get_activity_history(self, membership_type, membership_id, character_id=0, mode=0, count=10):
        """Gets activity history for indicated character
        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
            character_id (int) [optional]:
                The id of the character to retrieve stats for. If not provided, stats for all
                characters will be retrieved.
            mode (int) [optional]:
                The id of the game mode to include in the response
                (see Destiny.HistoricalStats.Definitions.DestinyActivityModeType).
        """
        url = DESTINY2_URL + '{}/Account/{}/Character/{}/Stats/Activities/?count={}&mode={}'
        url = url.format(membership_type, membership_id, character_id, count, mode)
        return await self._get_request(url)

    async def get_public_milestone_content(self, milestone_hash):
        """Gets custom localized content for the milestone of
        the given hash, if it exists.

        Args:
            milestone_hash (int):
                A valid hash id of a Destiny 2 milestone

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + f'Milestones/{milestone_hash}/Content/'
        return await self._get_request(url)

    async def get_public_milestones(self):
        """Gets information about the current public Milestones

        Returns:
            json (dict)
        """
        url = DESTINY2_URL + 'Milestones/'
        return await self._get_request(url)

    async def get_groups_for_member(self, membership_type, membership_id):
        """Gets information about the groups an individual member has joined

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID

        Returns:
            json(dict)
        """
        # /{membershipType}/{membershipId}/ | 0(NO FILTER)/1(CLANS)
        url = GROUP_URL + f'User/{membership_type}/{membership_id}/0/1/'
        return await self._get_request(url)

    async def get_group_members(self, group_id):
        """Gets list of members in a group

        Args:
            group_id (int):
                The id of the group

        Returns:
            json(dict)
        """
        url = GROUP_URL + '{}/Members/'
        url = url.format(group_id)
        return await self._get_request(url)

    async def get_weekly_milestones(self, group_id):
        """Gets the weekly milestones for a clan

        Args:
            group_id (int):
                The id of the group

        returns json(dict)
        """
        # /Clan/{groupId}/WeeklyRewardState/
        url = DESTINY2_URL + f'Clan/{group_id}/WeeklyRewardState/'
        # using the returned json
        return await self._get_request(url)

    async def get_milestone_definitions(self, milestone_hash):
        """Gets the milestones definition for a given milestoneHash

        Args:
            milestone_hash (int):
                The hash value that represents the milestone within the manifest

        returns json(dict)
        """
        # /Manifest/DestinyMilestoneDefinition/{milestoneHash}
        url = DESTINY2_URL + f'Manifest/DestinyMilestoneDefinition/{milestone_hash}'
        return await self._get_request(url)
    
    
    async def get_vendors(self, membership_type, membership_id, character_id, components):
        """Get currently available vendors from the list of vendors that can possibly have rotating
        inventory. Note that this does not include things like preview vendors and vendors-as-kiosks,
        neither of whom have rotating/dynamic inventories. Use their definitions as-is for those.

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
            character_id (int):
                The ID of the character to retrieve vendors for
            components (list):
                A list containing the components to include in the response
                (see Destiny.Responses.DestinyItemResponse). At least one
                component is required to receive results. Can use either ints
                or strings.

        Returns:
            json (dict)
        """
        payload = {'components': ','.join([str(i) for i in components])}
        url = DESTINY2_URL + f'{membership_type}/Profile/{membership_id}/Character/{character_id}/Vendors/'
        return await self._get_request(url, payload)

    
    async def get_vendor(self, membership_type, membership_id, character_id, vendor_hash, components):
        """Get the details of a specific Vendor.

        Args:
            membership_type (int):
                A valid non-BungieNet membership type (BungieMembershipType)
            membership_id (int):
                Destiny membership ID
            character_id (int):
                The ID of the character to retrieve vendor for
            vendor_hash (int):
                The hash of the vendor to retrieve
            components (list):
                A list containing the components to include in the response
                (see Destiny.Responses.DestinyItemResponse). At least one
                component is required to receive results. Can use either ints
                or strings.

        Returns:
            json (dict)
        """
        payload = {'components': ','.join([str(i) for i in components])}
        url = DESTINY2_URL + f'{membership_type}/Profile/{membership_id}/Character/{character_id}/Vendors/{vendor_hash}/'
        return await self._get_request(url, payload)
