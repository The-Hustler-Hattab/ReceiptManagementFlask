
from flask import Flask
from dotenv import load_dotenv
import os
from flasgger import Swagger
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth


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
app.config[Constants.ADMIN_GROUP] = os.getenv(Constants.ADMIN_GROUP)

# load swagger
swagger = Swagger(app)
allowed_domains = ['https://hattab-llc.mtattab.com', 'http://localhost:4200', 'http://127.0.0.1:4200']

CORS(app, resources={r"/*": {"origins": allowed_domains}}, allow_headers="*")

OKTA_JWK_URL = app.config.get(Constants.OIDC_JWK_URL)








# Import routes after creating the app instance to avoid circular imports
from app import routes
from app.controller import analytics_controller
from app.controller import blob_controller
from app.controller import receipts_controller
