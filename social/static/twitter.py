from datetime import datetime

def safe_int(val, default=0):
    try:
        return int(val)
    except:
        return default

def normalize_twitter_post(data):
    if data is None:
        return {
            "post_url": "",
            "post_text": "",
            "post_date": None,
            "post_time": None,
            "views": 0,
            "likes": 0,
            "comments_count": 0,
            "replies_count": 0,
            "shares": 0,
            "total_engagement": 0,
            "media_type": "none",
            "media_count": 0,
            "hashtags": []
        }

    post_date, post_time = None, None
    try:
        if "created_at" in data and data["created_at"]:
            dt = datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S %z %Y")
            post_date = dt.strftime("%Y-%m-%d")
            post_time = dt.strftime("%H:%M:%S")
    except Exception as e:
        # Fallback date parsing if the standard format fails
        parts = data.get("created_at", "").split()
        if len(parts) >= 5:
            # Make sure to use the correct indices for year, month, day
            post_date = f"{parts[5]}-{parts[1]}-{parts[2]}"
            post_time = parts[3]

    # Safely extract numeric values
    likes = safe_int(data.get("favorite_count", 0))
    comments_count = safe_int(data.get("reply_count", 0))
    shares = safe_int(data.get("retweet_count", 0))
    replies_count = safe_int(data.get("reply_count", 0))
    
    # Handle string view counts
    views_count = data.get("views_count", "0")
    views = safe_int(views_count, 0)

    media_type = "none"
    media_count = 0
    
    # Properly handle extended_entities which could be None
    if data.get("extended_entities") is not None and data["extended_entities"] is not None:
        if "media" in data["extended_entities"] and data["extended_entities"]["media"]:
            media_list = data["extended_entities"]["media"]
            if isinstance(media_list, list) and media_list:
                # Get type from the first media item
                media_type = media_list[0].get("type", "photo")
                media_count = len(media_list)

    # Extract hashtags correctly
    hashtags = []
    if data.get("entities") and "hashtags" in data["entities"]:
        for ht in data["entities"]["hashtags"]:
            if isinstance(ht, dict) and "text" in ht:
                hashtags.append(f"#{ht['text']}")
            elif isinstance(ht, str):
                hashtags.append(ht)

    total_engagement = likes + comments_count + shares

    return {
        "post_url": data.get("url", ""),
        "post_text": data.get("full_text", ""),
        "post_date": post_date,
        "post_time": post_time,
        "views": views,
        "likes": likes,
        "comments_count": comments_count,
        "replies_count": replies_count,
        "shares": shares,
        "total_engagement": total_engagement,
        "media_type": media_type,
        "media_count": media_count,
        "hashtags": hashtags
    }