import re
import requests

def extract_github_url(text):
    match = re.search(r'https?://github\.com/\S+', text)
    return match.group(0) if match else None

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
