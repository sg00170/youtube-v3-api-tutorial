import os

import google_auth_oauthlib
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
GOOGLE_ADS_LOGIN_CUSTOMER_ID = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")

SCOPES = ["https://www.googleapis.com/auth/adwords"]
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
        "login_customer_id": GOOGLE_ADS_LOGIN_CUSTOMER_ID,
        "use_proto_plus": True,
    }


def create_test_account(client: GoogleAdsClient):
    customer_service = client.get_service("CustomerService")

    customer = client.get_type("Customer")
    customer.descriptive_name = "Test Account"
    customer.currency_code = "KRW"
    customer.time_zone = "Asia/Seoul"

    response = customer_service.create_customer_client(
        customer_id=GOOGLE_ADS_LOGIN_CUSTOMER_ID,
        customer_client=customer,
    )
    print(f"✅ 테스트 계정 생성 완료: {response.resource_name}")


try:
    client = GoogleAdsClient.load_from_dict(get_authenticated_service())
    create_test_account(client)
except RefreshError:
    print("❌ OAuth 인증 실패: credentials.json 확인 필요")
except Exception as e:
    print(f"❌ 오류 발생: {e}")
