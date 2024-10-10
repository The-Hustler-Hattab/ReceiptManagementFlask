import logging

import plaid
from flask import Flask
from dotenv import load_dotenv
import os
from flasgger import Swagger
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from plaid.api import plaid_api


class Constants:
    DEBUG = 'DEBUG'
    MYSQL_URL = 'MYSQL_URL'
    TOGETHER_AI_API_KEY = 'TOGETHER_AI_API_KEY'
    OIDC_JWK_URL = 'OIDC_JWK_URL'
    AZURE_FORM_RECOGNIZER_ENDPOINT = 'AZURE_FORM_RECOGNIZER_ENDPOINT'
    AZURE_FORM_RECOGNIZER_KEY = 'AZURE_FORM_RECOGNIZER_KEY'
    APP_NAME = 'Receipts Service'
    BLOB_CONTAINER_NAME = 'BLOB_CONTAINER_NAME'
    BLOB_CONNECTION_STRING = 'BLOB_CONNECTION_STRING'
    ADMIN_GROUP = 'ADMIN_GROUP'
    BLOB_CONTAINER_SHERIF_SALE = 'BLOB_CONTAINER_SHERIF_SALE'
    QUEUE_SHERIF_SALE = 'QUEUE_SHERIF_SALE'
    AZURE_FORM_RECOGNIZER_MODEL_ID = 'AZURE_FORM_RECOGNIZER_MODEL_ID'
    PLAID_CLIENT_ID = 'PLAID_CLIENT_ID'
    PLAID_SECRET = 'PLAID_SECRET'
    BLOB_CONTAINER_INCOME = 'BLOB_CONTAINER_INCOME'

app = Flask(__name__)
oauth = OAuth(app)

# Load environment variables from .env file
load_dotenv()

# Set debug environment variable
app.config[Constants.DEBUG] = os.getenv(Constants.DEBUG)
app.config[Constants.MYSQL_URL] = os.getenv(Constants.MYSQL_URL)
app.config[Constants.TOGETHER_AI_API_KEY] = os.getenv(Constants.TOGETHER_AI_API_KEY)
app.config[Constants.OIDC_JWK_URL] = os.getenv(Constants.OIDC_JWK_URL)
app.config[Constants.AZURE_FORM_RECOGNIZER_ENDPOINT] = os.getenv(Constants.AZURE_FORM_RECOGNIZER_ENDPOINT)
app.config[Constants.AZURE_FORM_RECOGNIZER_KEY] = os.getenv(Constants.AZURE_FORM_RECOGNIZER_KEY)
app.config[Constants.BLOB_CONTAINER_NAME] = os.getenv(Constants.BLOB_CONTAINER_NAME)
app.config[Constants.BLOB_CONNECTION_STRING] = os.getenv(Constants.BLOB_CONNECTION_STRING)
app.config[Constants.BLOB_CONTAINER_SHERIF_SALE] = os.getenv(Constants.BLOB_CONTAINER_SHERIF_SALE)
app.config[Constants.QUEUE_SHERIF_SALE] = os.getenv(Constants.QUEUE_SHERIF_SALE)
app.config[Constants.ADMIN_GROUP] = os.getenv(Constants.ADMIN_GROUP)
app.config[Constants.AZURE_FORM_RECOGNIZER_MODEL_ID] = os.getenv(Constants.AZURE_FORM_RECOGNIZER_MODEL_ID)
app.config[Constants.PLAID_CLIENT_ID] = os.getenv(Constants.PLAID_CLIENT_ID)
app.config[Constants.PLAID_SECRET] = os.getenv(Constants.PLAID_SECRET)
app.config[Constants.BLOB_CONTAINER_INCOME] = os.getenv(Constants.BLOB_CONTAINER_INCOME)

# load swagger
swagger = Swagger(app)

# security configuration
allowed_domains = ['https://hattab-llc.mtattab.com', 'http://localhost:4200', 'http://127.0.0.1:4200']
CORS(app, resources={r"/*": {"origins": allowed_domains}}, allow_headers="*")
OKTA_JWK_URL = app.config.get(Constants.OIDC_JWK_URL)

#  logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Add timestamp format
    datefmt='%Y-%m-%d %H:%M:%S'  # Customize the date format
)


# plaid initial configuration
configuration = plaid.Configuration(
    # host=plaid.Environment.Sandbox,
    host=plaid.Environment.Production,

    api_key={
        'clientId': app.config.get(Constants.PLAID_CLIENT_ID),
        'secret': app.config.get(Constants.PLAID_SECRET),
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


# Import routes after creating the app instance to avoid circular imports
from app import routes
from app.controller import analytics_controller
from app.controller import blob_controller
from app.controller import receipts_controller
from app.controller import sherief_sale_controller
from app.controller import plaid_controller
from app.controller import income_controller
