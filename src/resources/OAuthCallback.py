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

    @ft.render("/callback/index.html")
    def on_get(self, req, resp):

        # build token url
        token_uri = urlunparse(
            [
                getenv("OAUTH_URI_SCHEME"),
                getenv("OAUTH_URI_NETLOC"),
                getenv("OAUTH_TOKEN_URI_PATH"),
                None,
                None,
                None,
            ]
        )

        # build POST payload
        payload = {
            "client_secret": getenv("OAUTH_CLIENT_SECRET"),
            "client_id": getenv("OAUTH_CLIENT_ID"),
            "redirect_uri": getenv("OAUTH_CALLBACK_URI"),
            "grant_type": "authorization_code",
            "code": req.get_param("code"),
        }

        # exchange code for access
        token_response = requests.post(token_uri, data=payload).json()

        # use the access token to retrieve compound field information from the REST API
        headers = {"Authorization": "Bearer " + token_response["access_token"]}
        object_names = getenv("BF_CHECK_OBJECT_NAMES").split()

        bad_fields = []
        for object_name in object_names:
            query = f"""
            SELECT DeveloperName, DataType
            FROM EntityParticle
            WHERE DataType IN ('address', 'location')
            AND EntityDefinitionId = '{object_name}'
            """

            bad_field_recs = requests.get(
                token_response["instance_url"]
                + f"/services/data/v{getenv('BF_CHECK_API_VERSION')}/query/?q={query}",
                headers=headers,
            ).json()["records"]

            if len(bad_field_recs) > 0:
                bad_fields += [
                    f"{object_name}.{x['DeveloperName']}" for x in bad_field_recs
                ]

        # Revoke the access code we've been using because security
        revoke_uri = urlunparse(
            [
                getenv("OAUTH_URI_SCHEME"),
                getenv("OAUTH_URI_NETLOC"),
                getenv("OAUTH_REVOKE_URI_PATH"),
                None,
                None,
                None,
            ]
        )

        requests.post(revoke_uri, data={"token": token_response["access_token"]})

        # set the context to use in the template
        resp.context = token_response
        resp.context.update(
            {
                "state": req.get_param("state"),
                "code": req.get_param("code"),
                "bad_fields": json.dumps(bad_fields, indent=4, sort_keys=True),
                "sf_objects": object_names,
            }
        )
