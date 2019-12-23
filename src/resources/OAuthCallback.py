import requests
import json
from falcon_jinja2 import FalconTemplate
from os import getenv
from urllib.parse import urlunparse


class OAuthCallbackResource(object):
    """
    Handles the callback from the IDP
    """

    ft = FalconTemplate()

    @ft.render('/callback/index.html')
    def on_get(self, req, resp):
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

        # exchange code for access
        token_response = requests.post(token_uri, data=payload).json()

        # use the access token to retrieve some information from the Lightning REST API
        headers = {'Authorization': 'Bearer ' + token_response['access_token']}

        lightning_response = requests.get(
            token_response['instance_url'] + '/services/data/v47.0/limits/',
            headers=headers
        ).json()

        # Revoke the access code we've been using because security
        revoke_uri = urlunparse([
            getenv('OAUTH_URI_SCHEME'),
            getenv('OAUTH_URI_NETLOC'),
            getenv('OAUTH_REVOKE_URI_PATH'),
            None,
            None,
            None
        ])

        requests.post(
            revoke_uri,
            data={'token': token_response['access_token']}
        )

        # set the context to use in the template
        resp.context = token_response
        resp.context.update({
            'state': req.get_param('state'),
            'code': req.get_param('code'),
            'sf_limits': json.dumps(lightning_response, indent=4, sort_keys=True)
        })
