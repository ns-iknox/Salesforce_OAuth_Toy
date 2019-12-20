import requests
import json
from os import getenv
from urllib.parse import urlunparse


class OAuthCallbackResource(object):
    """
    Handles the callback from the IDP
    """

    @staticmethod
    def on_get(req, resp):
        # build token url
        token_uri = urlunparse([
            getenv('OAUTH_URI_SCHEME'),
            getenv('OAUTH_URI_NETLOC'),
            getenv('OAUTH_TOKEN_URI_PATH'),
            None,
            None,
            None
        ])

        # build POST payload
        payload = {
            'client_secret': getenv('OAUTH_CLIENT_SECRET'),
            'client_id': getenv('OAUTH_CLIENT_ID'),
            'redirect_uri': getenv('OAUTH_CALLBACK_URI'),
            'grant_type': 'authorization_code',
            'code': req.get_param('code')
        }

        # exchange code for access token
        token_response = requests.post(token_uri, data=payload)

        resp.body = json.dumps(token_response.json())
