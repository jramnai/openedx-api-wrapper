"""Open edX REST API Python Client"""

from __future__ import absolute_import, unicode_literals

from openedx_api_wrapper import components, util

COMPONENT_CLASSES = {
    "user": components.user.UserComponent,
}


class OpenedxAPIClient(util.ApiClient):
    """
    API client for Open edX LMS/Studio (a.k.a. edxapp / edx-platform)

    Use this to connect to Open edX as a service user (as your backend application).
    """

    def __init__(self, lms_url, studio_url, oauth_key, oauth_secret):
        """
        Initialize this Open edX API client
        """
        self.components = COMPONENT_CLASSES.copy()
        super(OpenedxAPIClient, self).__init__(lms_url, studio_url, oauth_key, oauth_secret)

        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](
                lms_url,
                studio_url,
                oauth_key,
                oauth_secret
            )

    @property
    def user(self):
        """Get the user component"""
        return self.components.get("user")
