from urllib.parse import urlparse, parse_qs
import re


def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.netloc == "youtu.be":
        return parsed.path.lstrip("/")
    if "youtube.com" in parsed.netloc:
        qs = parse_qs(parsed.query)
        return qs.get("v", [None])[0]
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)

    return match.group(1) if match else None

def extract_comment_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    lc_value = query_params.get("lc", [None])[0]

    return lc_value if lc_value else None