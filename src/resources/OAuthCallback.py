import requests

from falcon_jinja2 import FalconTemplate
from os import getenv
from urllib.parse import urlunparse


class OAuthCallbackResource(object):
    """
    Handles the callback from the IDP
    """

    ft = FalconTemplate()

    @ft.render('/callback/index.html')
    def on_get(_, req, resp):
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

        # set the context to use in the template
        resp.context = token_response
        resp.context.update({
            'state': req.get_param('state'),
            'code': req.get_param('code')
        })
