from urllib.parse import urlunparse
from urllib.parse import urlencode
from falcon_jinja2 import FalconTemplate
from os import getenv
from uuid import uuid4


class LoginResource(object):
    """
    Builds the login URL and serves up the jinja2 template that uses it.
    """
    ft = FalconTemplate()

    @ft.render('/login/index.html')
    def on_get(self, _, resp):
        # build query string
        qs_dict = {
            'response_type': 'code',
            'client_id': getenv('OAUTH_CLIENT_ID'),
            'redirect_uri': getenv('OAUTH_CALLBACK_URI'),
            'scope': getenv('OAUTH_SCOPE'),
            'state': getenv('OAUTH_STATE', uuid4()),
        }
        query_string = urlencode(qs_dict)

        # build login URL
        login_url = urlunparse([
            getenv('OAUTH_URI_SCHEME'),
            getenv('OAUTH_URI_NETLOC'),
            getenv('OAUTH_LOGIN_URI_PATH'),
            None,
            query_string,
            None
        ])

        # set context for renderer
        resp.context = {
                        'login_url': login_url,
                        'state': qs_dict['state']
                        }
