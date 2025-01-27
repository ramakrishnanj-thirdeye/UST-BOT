import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    APP_ID = os.getenv("MICROSOFT_APP_ID")
    APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")
    PROMPT_FLOW_URL = os.getenv("PROMPT_FLOW_URL")
    PROMPT_FLOW_API_KEY = os.getenv("PROMPT_FLOW_API_KEY")
    AAD_CONNECTION_NAME = os.getenv("AAD_CONNECTION_NAME")  # Azure AD OAuth connection
