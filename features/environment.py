from dotenv import load_dotenv
import os

def before_all(context):
    # Load environment variables from .env file
    load_dotenv()
    context.api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    context.cx = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_CX")
