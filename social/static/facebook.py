from datetime import datetime 
import re

def safe_int(val, default=0):
    try:
        return int(val)
    except:
        return default
    

def extract_hashtags(text: str):
    return re.findall(r"#\w+", text) if text else []

def normalize_facebook_post(data):
    post_date, post_time = None, None
    try:
        if "creationDate" in data:
            dt = datetime.strptime(data["creationDate"], "%A, %B %d, %Y at %I:%M %p")
            post_date = dt.strftime("%Y-%m-%d")
            post_time = dt.strftime("%H:%M:%S")
    except:
        if "creationDate" in data:
            parts = data["creationDate"].split(" at ")
            if len(parts) == 2:
                post_date, post_time = parts[0], parts[1]

    likes = safe_int(data.get("reactionCount", 0))
    comments_count = safe_int(data.get("commentComment", 0))
    shares = safe_int(data.get("shareCount", 0))
    views = safe_int(data.get("videoViewCount", 0))

    media_type = "none"
    media_count = 0
    if data.get("imageUrlList"):
        media_type = "image"
        media_count = len(data["imageUrlList"])
    elif views > 0:
        media_type = "video"
        media_count = 1

    return {
        "post_url": data.get("postUrl", ""),
        "post_text": data.get("text", ""),
        "post_date": post_date,
        "post_time": post_time,
        "views": views,
        "likes": likes,
        "comments_count": comments_count,
        "replies_count": 0,  # Facebook reply count not given
        "shares": shares,
        "total_engagement": likes + comments_count + shares,
        "media_type": media_type,
        "media_count": media_count,
        "hashtags": extract_hashtags(data.get("text", ""))
    }