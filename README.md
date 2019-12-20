# OAuth 2.0 code flow for Salesforce
## (a toy implementation)
### Setup

* Log in to salesforce and configure a new connected app (@TODO provide tutorial link).

Within your virtual environment of choice...
* Install the requirements: `pip install -r requirements.txt -r requirements-dev.txt`
* Configure the app `cp .env-example .env && vi .env` 
    (must provide minimally a Client ID and Client Secret from SF)

### Running the toy
`./start`
Point your browser to `http://localhost:8000` and follow the provided link!

@TODO: Actually query the API to prove it works.