import re

def extract_skills(text):
    # Example tech keywords; expand this list
    keywords = ['python', 'java', 'aws', 'docker', 'streamlit', 'sql']
    text = text.lower()
    found = [kw for kw in keywords if kw in text]
    return list(set(found))
