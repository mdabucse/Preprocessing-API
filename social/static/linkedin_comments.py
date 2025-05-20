from static.safe import safe_int

def normalize_linkedin_comment(data):
    """
    Normalize a LinkedIn comment into a standardized format.
    
    Args:
        data (dict): The LinkedIn comment data
        
    Returns:
        dict: Normalized comment data
    """
    if data is None:
        return {
            "comment_id": "",
            "comment_text": "",
            "comment_date": None,
            "comment_time": None,
            "comment_url": "",
            "author_name": "",
            "author_headline": "",
            "author_profile_url": "",
            "likes": 0,
            "total_reactions": 0,
            "replies_count": 0,
            "is_edited": False,
            "is_pinned": False,
            "post_id": ""
        }
    
    # Extract date and time
    post_date, post_time = None, None
    if "posted_at" in data and "date" in data["posted_at"]:
        parts = data["posted_at"]["date"].split()
        if len(parts) >= 2:
            post_date, post_time = parts[0], parts[1]
    
    # Extract author information
    author_name = ""
    author_headline = ""
    author_profile_url = ""
    if "author" in data:
        author_name = data["author"].get("name", "")
        author_headline = data["author"].get("headline", "")
        author_profile_url = data["author"].get("profile_url", "")
    
    # Extract reaction stats
    total_reactions = 0
    likes = 0
    if "stats" in data:
        total_reactions = safe_int(data["stats"].get("total_reactions", 0))
        if "reactions" in data["stats"]:
            likes = safe_int(data["stats"]["reactions"].get("like", 0))
    
    # Count replies
    replies_count = 0
    if "replies" in data:
        replies_count = len(data["replies"]) if data["replies"] else 0
    
    return {
        "comment_id": data.get("comment_id", ""),
        "comment_text": data.get("text", ""),
        "comment_date": post_date,
        "comment_time": post_time,
        "comment_url": data.get("comment_url", ""),
        "author_name": author_name,
        "author_headline": author_headline,
        "author_profile_url": author_profile_url,
        "likes": likes,
        "total_reactions": total_reactions,
        "replies_count": replies_count,
        "is_edited": data.get("is_edited", False),
        "is_pinned": data.get("is_pinned", False),
        "post_id": data.get("post_input", "")
    }