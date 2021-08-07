"""Open edX REST API Python Client -- User component"""

from __future__ import absolute_import

from openedx_api_wrapper.components import base


class UserComponent(base.BaseComponent):
    """Component dealing with all user related matters"""

    def get_username(self, required=True) -> str:
        """
        Get the LMS/Studio username being used to make API requests.

        If this API client cannot make authenticated calls to the Open edX API,
        this will raise an exception, unless required is False, in which case it
        will just return None.
        """
        response = self.call_lms_raw('get', '/api/user/v1/me')
        if required:
            response.raise_for_status()
        else:
            if response.status_code == 401:
                return None
        return response.json()["username"]

    def get_user_details(self, username):
        """
        Get a user's profile.
        """
        return self.call_lms('get', f'/api/user/v1/accounts/{username}')

    def registration(self, data):
        """
        User registration
        """
        return self.call_lms('post', '/api/user/v1/account/registration/', data=data)
