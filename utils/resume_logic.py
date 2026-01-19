from utils.llm import enhance_text
from ats import enhance_with_keywords


def build_resume(data):
    """
    Builds clean, structured resume content.
    NO fake data.
    NO assumptions.
    """

    summary = enhance_text(data["summary"], data["role"])
    summary = enhance_with_keywords(summary)

    resume_content = {
        "name": data["name"],
        "role": data["role"],
        "email": data["email"],
        "linkedin": data["linkedin"],

        "skills": data["skills"],
        "projects": data["projects"],
        "experience": data["experience"],
        "education": data["education"],
    }

    return resume_content
