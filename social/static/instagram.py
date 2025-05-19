import re
from datetime import datetime
def safe_int(val, default=0):
    try:
        return int(val)
    except:
        return default

def extract_hashtags(text: str):
    return re.findall(r"#\w+", text) if text else []
def normalize_instagram_post(data):
    post_date, post_time = None, None
    try:
        if "timestamp" in data:
            dt_format = "%Y-%m-%dT%H:%M:%S.%fZ" if "." in data["timestamp"] else "%Y-%m-%dT%H:%M:%S%z"
            dt = datetime.strptime(data["timestamp"], dt_format)
            post_date = dt.strftime("%Y-%m-%d")
            post_time = dt.strftime("%H:%M:%S")
    except:
        parts = data.get("timestamp", "").split("T")
        if len(parts) == 2:
            post_date = parts[0]
            post_time = parts[1].split("+")[0] if "+" in parts[1] else parts[1]

    likes = safe_int(data.get("likesCount", 0))
    comments_count = safe_int(data.get("commentsCount", 0))
    views = safe_int(data.get("videoViewCount", 0) or data.get("videoPlayCount", 0))
    shares = 0  # Instagram shares count not available

    media_type = "none"
    media_count = 0
    if "type" in data and data["type"]:
        media_type = data["type"].lower()
        media_count = 1
    elif "media_type" in data and data["media_type"]:
        media_type = data["media_type"].lower()
        media_count = 1

    if media_type == "carousel_album" and "childPosts" in data:
        media_count = len(data["childPosts"]) if data["childPosts"] else 1

    return {
        "post_url": data.get("url") or data.get("permalink", ""),
        "post_text": data.get("caption", ""),
        "post_date": post_date,
        "post_time": post_time,
        "views": views,
        "likes": likes,
        "comments_count": comments_count,
        "replies_count": 0,
        "shares": shares,
        "total_engagement": likes + comments_count,
        "media_type": media_type,
        "media_count": media_count,
        "hashtags": extract_hashtags(data.get("caption", ""))
    }