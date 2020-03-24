# OAuth 2.0 code flow for Salesforce
## (a toy implementation)
### Setup

* Log in to Salesforce and create a [new connected app](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_defining_remote_access_applications.htm).

Within your virtual environment of choice...
* Install the requirements: `pip install -r requirements.txt -r requirements-dev.txt`
* Configure the app `cp .env-example .env && vi .env` (must provide minimally a Client ID and Client Secret from SF)

### Running the toy
* Start the local web server `./start`
* Point your browser to `http://localhost:8000` and follow the provided link!
* Note: Refreshing the results page will not work (the key is invalidated for security purposes)