import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

from utils import extract_video_id

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_LINK = os.getenv("YOUTUBE_LINK")
VIDEO_ID = extract_video_id(YOUTUBE_LINK)

youtube = build("youtube", "v3", developerKey=API_KEY)

video_response = youtube.videos().list(part="snippet,statistics", id=VIDEO_ID).execute()
video = video_response["items"][0]
title = video["snippet"]["title"]
description = video["snippet"]["description"]
view_count = video["statistics"]["viewCount"]
category_id = video["snippet"]["categoryId"]
print(f"제목: {title}")
print(f"설명: {description}")
print(f"조회수: {view_count}")
print(f"카테고리 ID: {category_id}")

category_response = (
    youtube.videoCategories()
    .list(
        part="snippet",
        id=category_id,
    )
    .execute()
)
category_title = category_response["items"][0]["snippet"]["title"]
print(f"카테고리 이름: {category_title}")

comments_response = (
    youtube.commentThreads()
    .list(part="snippet", videoId=VIDEO_ID, maxResults=10, textFormat="plainText")
    .execute()
)
print("\n📌 댓글 목록:")
for item in comments_response["items"]:
    comment_snippet = item["snippet"]["topLevelComment"]["snippet"]
    text = comment_snippet["textDisplay"]
    published_at = comment_snippet["publishedAt"]
    updated_at = comment_snippet.get("updatedAt", "수정되지 않음")
    print(f"- 댓글: {text}")
    print(f"  작성일: {published_at}, 수정일: {updated_at}\n")
