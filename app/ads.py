import os

import google_auth_oauthlib
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

load_dotenv()

GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
GOOGLE_ADS_LOGIN_CUSTOMER_ID = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
GOOGLE_ADS_CUSTOMER_ID = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

SCOPES = ["https://www.googleapis.com/auth/adwords"]
API_SERVICE_NAME = "googleads"
API_VERSION = "v16"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "credentials.json")


def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    credentials = flow.run_local_server(
        port=8000, access_type="offline", prompt="consent"
    )

    return {
        "developer_token": GOOGLE_ADS_DEVELOPER_TOKEN,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "refresh_token": credentials.refresh_token,
        "use_proto_plus": True,
        "login_customer_id": GOOGLE_ADS_LOGIN_CUSTOMER_ID,
    }


client = GoogleAdsClient.load_from_dict(get_authenticated_service())
ga_service = client.get_service("GoogleAdsService")
# https://developers.google.com/google-ads/api/fields/v16/customer
query = """
    SELECT
        customer.id,
        customer.descriptive_name,
        customer.linked_youtube_channels.channel_id
    FROM customer
"""

response = ga_service.search_stream(customer_id=GOOGLE_ADS_CUSTOMER_ID, query=query)

for batch in response:
    for row in batch.results:
        print(f"Customer ID: {row.customer.id}")
        for channel in row.customer.linked_youtube_channels:
            print(f"Linked YouTube Channel ID: {channel.channel_id}")
