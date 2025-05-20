def normalize_linkedin_profile(profile):
    """
    Normalizes LinkedIn profile data for LLM inputs.
    
    Args:
        profile (dict): The LinkedIn profile data
        
    Returns:
        dict: Normalized profile data
    """
    # Extract the profile from the list if needed
    if isinstance(profile, list) and len(profile) > 0:
        profile = profile[0]
    
    normalized = {}
    
    # Basic information
    normalized['name'] = profile.get('name', '')
    normalized['linkedin_url'] = profile.get('url', '')
    
    # Handle location
    city = profile.get('city', '')
    country_code = profile.get('country_code', '')
    normalized['location'] = f"{city}, {country_code}" if city and country_code else city or country_code
    
    # Current position and company
    normalized['current_position'] = profile.get('position', '')
    
    current_company = profile.get('current_company', {})
    if isinstance(current_company, dict):
        normalized['current_company'] = current_company.get('name', '')
    else:
        normalized['current_company'] = current_company
    
    # About section
    normalized['about'] = profile.get('about', '')
    
    # Social metrics
    normalized['followers'] = profile.get('followers', 0)
    normalized['connections'] = profile.get('connections', 0)
    
    # Experience
    normalized['experience'] = []
    for exp in profile.get('experience', []):
        normalized['experience'].append({
            'title': exp.get('title', ''),
            'company': exp.get('company', ''),
            'location': exp.get('location', ''),
            'start_date': exp.get('start_date', ''),
            'end_date': exp.get('end_date', ''),
            'description': exp.get('description', '')
        })
    
    # Education
    normalized['education'] = []
    for edu in profile.get('education', []):
        normalized['education'].append({
            'title': edu.get('title', ''),
            'degree': edu.get('degree', ''),
            'url': edu.get('url', '')
        })
    
    # Activity
    normalized['activity'] = []
    for act in profile.get('activity', []):
        normalized['activity'].append({
            'title': act.get('title', ''),
            'link': act.get('link', '')
        })
    
    return normalized
