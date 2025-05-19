import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from static.twitter import normalize_twitter_post
def extract_hashtags(text: str):
    return re.findall(r"#\w+", text) if text else []

def safe_int(val, default=0):
    try:
        return int(val)
    except:
        return default

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

def normalize_social_post(data, platform):
    platform = platform.lower()
    if platform == "linkedin":
        return normalize_linkedin_post(data)
    elif platform == "facebook":
        return normalize_facebook_post(data)
    elif platform == "twitter" or platform == "x":
        return normalize_twitter_post(data)
    elif platform == "instagram":
        return normalize_instagram_post(data)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

def process_and_normalize(data_list, platform):
    """Process and normalize a list of social media posts for a specific platform"""
    normalized = []
    if data_list is None:
        print(f"Warning: No data provided for {platform}")
        return normalized
        
    for post in data_list:
        try:
            if post is None:
                print(f"Warning: Encountered None post for {platform}, skipping")
                continue
            result = normalize_social_post(post, platform)
            normalized.append(result)
        except Exception as e:
            print(f"Error normalizing {platform} post: {str(e)}")
    return normalized


def export_normalized_data(data, output_file, format="json"):
    """Export normalized data to a file in the specified format"""
    if format.lower() == "json":
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif format.lower() == "csv":
        import csv
        
        # Flatten nested dictionaries for CSV export
        flattened_data = []
        for platform, posts in data.items():
            for post in posts:
                flat_post = {"platform": platform}
                for key, value in post.items():
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            flat_post[f"{key}_{sub_key}"] = sub_value
                    else:
                        flat_post[key] = value
                flattened_data.append(flat_post)
        
        if flattened_data:
            fieldnames = flattened_data[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flattened_data)
    else:
        raise ValueError(f"Unsupported export format: {format}")

def main():
    try:
        # Load input data
        input_file = r"A:\Adya\social\Data\social.json"  # Change this to your input file
        output_file = r"A:\Adya\social\Data\normalized_social_data.json"  # Change this to your desired output file
        export_format = "json"  # or "csv"
        
        print(f"Loading data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Extract data for each platform
        linkedin_data = data.get("linkedin", [])
        facebook_data = data.get("facebook", [])
        twitter_data = data.get("twitter", [])
        instagram_data = data.get("instagram", [])
        # Process and normalize data for each platform
        print("Normalizing data...")
        normalized_data = {
            "linkedin": process_and_normalize(linkedin_data, "linkedin"),
            "facebook": process_and_normalize(facebook_data, "facebook"),
            "twitter": process_and_normalize(twitter_data, "twitter"),
            "instagram": process_and_normalize(instagram_data, "instagram")
        }
        
        # Export normalized data
        print(f"Exporting normalized data to {output_file}...")
        export_normalized_data(normalized_data, output_file, export_format)
        
        print(f"Successfully processed and exported normalized data to {output_file}")
        
        # Print some stats
        total_posts = sum(len(posts) for posts in normalized_data.values())
        print(f"Total normalized posts: {total_posts}")
        for platform, posts in normalized_data.items():
            print(f"  - {platform}: {len(posts)} posts")
            
    except FileNotFoundError as e:
        print(f"Error: Input file not found - {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in input file - {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
