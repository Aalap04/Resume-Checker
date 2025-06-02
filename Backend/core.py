
from Backend.text_loader import extract_text_from_pdf
from Backend.resume_parser import extract_skills
from Backend.similarity import calculate_similarity
from Backend.github_analyzer import extract_github_url, get_github_activity

def process_resume(resume_path, job_path):
    resume_text = extract_text_from_pdf(resume_path)
    job_text = extract_text_from_pdf(job_path)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    match_score = calculate_similarity(resume_text, job_text)

    github_url = extract_github_url(resume_text)
    github_info = {}
    if github_url:
        username = github_url.strip().split("github.com/")[-1].split("/")[0]
        github_info = get_github_activity(username)

    return {
        "match_score": round(match_score * 100, 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "github_profile": github_url,
        "github_analysis": github_info,
    }
