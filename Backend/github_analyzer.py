import re
import requests

def extract_github_url(text):
    # Updated pattern to match both https://github.com and github.com
    pattern = r'(?:https?://)?(?:www\.)?github\.com/\S+'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        url = match.group(0)
        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    return None

def get_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch GitHub activity"}
    
    events = response.json()
    return {
        "public_events": len(events),
        "recent_activity": [e['type'] for e in events[:5]]
    }
