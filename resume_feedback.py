def analyze_resume(text, skills):

    breakdown = {
        "Skills": 0,
        "Projects": 0,
        "Experience": 0,
        "Education": 0
    }

    tips = []

    # Skills Score
    if len(skills) >= 5:
        breakdown["Skills"] = 40
    else:
        breakdown["Skills"] = 20
        tips.append("Add more technical skills.")

    # Projects
    if "project" in text.lower():
        breakdown["Projects"] = 20
    else:
        tips.append("Add project section.")
    
    # Experience
    if "experience" in text.lower():
        breakdown["Experience"] = 20
    else:
        tips.append("Add experience section.")

    # Education
    if "education" in text.lower():
        breakdown["Education"] = 20
    else:
        tips.append("Add education details.")

    total_score = sum(breakdown.values())

    return breakdown, total_score, tips