import falcon

from dotenv import load_dotenv
from os import getenv

from src.resources import LoginResource
from src.resources import OAuthCallbackResource

# Load env vars
load_dotenv(dotenv_path='../.env')

app = falcon.API()
app.add_route('/callback', OAuthCallbackResource())
app.add_route('/', LoginResource())
