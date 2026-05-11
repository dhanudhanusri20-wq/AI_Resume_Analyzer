import re

def calculate_score(text, skills):

    score = 0

    # Skills Score
    score += len(skills) * 5

    # Email Check
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        score += 15

    # Phone Number Check
    if re.search(r"\d{10}", text):
        score += 15

    # Education Keywords
    education_keywords = [
        "bachelor",
        "master",
        "b.sc",
        "b.e",
        "b.tech",
        "mca",
        "mba"
    ]

    for word in education_keywords:
        if word.lower() in text.lower():
            score += 10
            break

    # Experience Keywords
    experience_keywords = [
        "project",
        "internship",
        "experience"
    ]

    for word in experience_keywords:
        if word.lower() in text.lower():
            score += 10
            break

    # Limit Score
    if score > 100:
        score = 100

    return score
