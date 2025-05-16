import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]
API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "credentials.json")

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8000, access_type='offline', prompt='consent')
    print(f"credentials: {credentials.to_json()}")
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_video_analytics(youtube_analytics, start_date, end_date):
    response = youtube_analytics.reports().query(
        ids="channel==MINE",
        startDate=start_date,
        endDate=end_date,
        metrics="views",
        dimensions="day",
        sort="day"
    ).execute()

    return response


youtube_analytics = get_authenticated_service()

start_date = "2025-01-01"
end_date = "2025-05-01"

analytics_data = get_video_analytics(youtube_analytics, start_date, end_date)
print(f"analytics_data: {analytics_data}")

for row in analytics_data.get("rows", []):
    video_id = row[0]
    ctr = row[1]
    avg_view_duration = row[2]
    print(f"Video ID: {video_id}, CTR: {ctr:.2%}, Avg View Duration: {avg_view_duration} seconds")