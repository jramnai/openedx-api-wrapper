"""Utility classes and functions"""

from __future__ import absolute_import, unicode_literals

import logging
import os

import requests
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session

log = logging.getLogger(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1" # TODO: Add this conditionally for the development environment only


class ApiClient(object):
    """Simple wrapper for REST API requests"""

    def __init__(self, lms_url, studio_url, oauth_key, oauth_secret):
        """
        Initialize this API client
        """
        self.lms_url = lms_url  # e.g. "http://edx.devstack.lms:18000"
        self.studio_url = studio_url  # e.g. "http://edx.devstack.studio:18010"
        self.client_oauth_key = oauth_key  # e.g. LMS_API_AUTH_KEY
        self.client_oauth_secret = oauth_secret  # e.g. LMS_API_AUTH_SECRET
        self.token_url = lms_url + '/oauth2/access_token'  # e.g. "http://edx.devstack.lms:18000/oauth2/access_token"
        self.session, refresh_now = self.init_session()
        if refresh_now:
            self.refresh_session_token()

    def init_session(self):
        """
        Initialize the HTTP session that this client will use.

        Returns the session and a boolean indicating if refresh_session_token
        should immediately be called, as opposed to calling it only after trying
        an API call and getting a 401 response.
        """
        client = BackendApplicationClient(client_id=self.client_oauth_key)
        return OAuth2Session(client=client), True

    def refresh_session_token(self):
        """
        Refreshes the authenticated session with a new token.
        """
        # We cannot use session.fetch_token() because it sends the client
        # credentials using HTTP basic auth instead of as POST form data.
        res = requests.post(self.token_url, data={
            'client_id': self.client_oauth_key,
            'client_secret': self.client_oauth_secret,
            'grant_type': 'client_credentials'
        })
        res.raise_for_status()
        data = res.json()
        self.session.token = {'access_token': data['access_token']}

    def call_lms_raw(self, method, path, **kwargs):
        """
        Make an LMS API call and return the HTTP response.
        """
        url = self.lms_url + path
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 401:
                raise TokenExpiredError
        except TokenExpiredError:
            self.refresh_session_token()
            response = self.session.request(method, url, **kwargs)

        return response

    def call_studio_raw(self, method, path, **kwargs):
        """
        Make a Studio API call and return the HTTP response.
        """
        url = self.studio_url + path
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 401:
                raise TokenExpiredError
        except TokenExpiredError:
            self.refresh_session_token()
            response = self.session.request(method, url, **kwargs)

        return response

    def call_lms(self, method, path, **kwargs):
        """
        Make an API call from the LMS. Returns the parsed JSON response.
        """
        response = self.call_lms_raw(method, path, **kwargs)
        if response.status_code == 400:
            log.error("400 Bad Request from LMS: %s", response.content)
        response.raise_for_status()
        if response.status_code == 204:  # No content
            return None
        return response.json()

    def call_studio(self, method, path, **kwargs):
        """
        Make an API call from Studio. Returns the parsed JSON response.
        """
        response = self.call_studio_raw(method, path, **kwargs)
        if response.status_code == 400:
            log.error("400 Bad Request from Studio: %s", response.content)
        response.raise_for_status()
        if response.status_code == 204:  # No content
            return None
        return response.json()
