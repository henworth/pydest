from pydest.base import _BaseAPI


class User(_BaseAPI):

    async def get_bungie_net_user_by_id(self, membership_id):
        """Loads a bungienet user by membership id

        Args:
            membership_id: The requested Bungie.net membership id

        Returns:
            json (dict)
        """
        url = f'{self.USER_URL}/GetBungieNetUserById/{membership_id}/'
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
        url = f'{self.USER_URL}/GetMembershipsById/{membership_id}/{membership_type}/'
        return await self._get_request(url)
