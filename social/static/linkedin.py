import re

def safe_int(val, default=0):
    try:
        return int(val)
    except:
        return default
def extract_hashtags(text: str):
    return re.findall(r"#\w+", text) if text else []
def normalize_linkedin_post(data):
    post_date, post_time = None, None
    if "posted_at" in data and "date" in data["posted_at"]:
        parts = data["posted_at"]["date"].split()
        if len(parts) >= 2:
            post_date, post_time = parts[0], parts[1]

    stats = data.get("stats", {})
    likes = safe_int(stats.get("like", 0))
    comments_count = safe_int(stats.get("comments", 0))
    shares = safe_int(stats.get("reposts", 0))
    total_engagement = safe_int(stats.get("total_reactions", 0))

    media_type = "none"
    media_count = 0
    if data.get("media"):
        media_type = data["media"].get("type", "none")
        media_count = len(data["media"].get("items", [])) if "items" in data["media"] else 0

    return {
        "post_url": data.get("post_url", ""),
        "post_text": data.get("text", ""),
        "post_date": post_date,
        "post_time": post_time,
        "views": 0,  # LinkedIn views not provided here
        "likes": likes,
        "comments_count": comments_count,
        "replies_count": 0,  # No replies data
        "shares": shares,
        "total_engagement": total_engagement,
        "media_type": media_type,
        "media_count": media_count,
        "hashtags": extract_hashtags(data.get("text", ""))
    }
