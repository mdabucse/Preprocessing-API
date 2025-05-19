from static.twitter import normalize_twitter_post
from static.instagram import normalize_instagram_post
from static.facebook import normalize_facebook_post
from static.linkedin import normalize_linkedin_post
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Union


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
