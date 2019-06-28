from pydest.base import _BaseAPI
from pydest.errors import PydestException

class Group(_BaseAPI):

    async def get_available_avatars(self):
        url = f'{self.GROUP_URL}/GetAvailableAvatars/'
        return await self._get_request(url)

    async def get_available_themes(self):
        url = f'{self.GROUP_URL}/GetAvailableThemes/'
        return await self._get_request(url)

    async def get_user_clan_invite_setting(self, membership_type, access_token):
        url = f'{self.GROUP_URL}/GetUserClanInviteSetting/{membership_type}/'
        return await self._get_request(url, access_token=access_token)

    async def get_recommended_groups(self, group_type, create_date_range, access_token):
        url = f'{self.GROUP_URL}/Recommended/{group_type}/{create_date_range}/'
        return await self._postt_request(url, access_token=access_token)

    async def search(self):
        # TODO
        url = f'{self.GROUP_URL}/Search/'

    async def get_by_id(self, group_id):
        """Get information about a specific group

        Path: /GroupV2/{group_id}/
        Verb: GET

        Args:
            group_id (int):
                The id of the group

        Returns:
            json (dict)
        """
        url = f'{self.GROUP_URL}/{group_id}/'
        return await self._get_request(url)

    async def get_by_name(self, group_name, group_type):
        if group_type not in [self.GROUP_TYPE_GENERAL, self.GROUP_TYPE_CLAN]:
            raise PydestException((
                f"Invalid group type {group_type}, must be one of "
                f"{self.GROUP_TYPE_GENERAL}, {self.GROUP_TYPE_CLAN}"))
        url = f'{self.GROUP_URL}/{group_name}/{group_type}/'
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
        url = f'{self.GROUP_URL}/User/{membership_type}/{membership_id}/{GROUP_FILTER_NONE}/{GROUP_TYPE_CLAN}/'
        return await self._get_request(url)

    async def get_group_members(self, group_id):
        """Gets list of members in a group

        Args:
            group_id (int):
                The id of the group

        Returns:
            json (dict)
        """
        url = f'{self.GROUP_URL}/{group_id}/Members/'
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
        url = f'{self.GROUP_URL}/{group_id}/Members/Pending/'
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
        url = f'{self.GROUP_URL}/{group_id}/Members/InvitedIndividuals/'
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
        url = f'{self.GROUP_URL}/{group_id}/Members/IndividualInvite/{membership_type}/{membership_id}/'
        return await self._post_request(url, data=data, access_token=access_token)

    async def group_invite_member_cancel(self, group_id, membership_type, membership_id, message, access_token):
        """Invite a user to join this group

        Path: /GroupV2/{group_id}/Members/IndividualInviteCancel/{membership_type}/{membership_id}/
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
        url = f'{self.GROUP_URL}/{group_id}/Members/IndividualInviteCancel/{membership_type}/{membership_id}/'
        return await self._post_request(url, data=data, access_token=access_token)

    async def group_pending_members_deny(self, group_id, membership_type, membership_id, message, access_token):
        """Invite a user to join this group

        Path: /GroupV2/{group_id}/Members/DenyList/
        Verb: POST

        Required Scope(s):
            oauth2: AdminGroups

        Args:
            group_id (int):
                The id of the group
            memberships (list):
                List of membership dicts to deny, structure of each:
                    membershipType (int):
                        A valid non-BungieNet membership type (BungieMembershipType)
                    membershipId (int):
                        The requested Bungie.net membership id
                    displayName (str):
                        The full gamertag or PSN id of the player. Spaces and case are ignored.
            message (str):
                Message to send along with the invite
            access_token (str):
                OAuth access token

        Returns:
            json(dict)
        """
        data = {'message': message, 'memberships': memberships}
        url = f'{self.GROUP_URL}/{group_id}/Members/DenyList/'
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
        url = f'{self.GROUP_URL}/{group_id}/Members/{membership_type}/{membership_id}/Kick/'
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
        url = f'{self.GROUP_URL}/{group_id}/Members/Approve/{membership_type}/{membership_id}/'
        return await self._post_request(url, data=data, access_token=access_token)
