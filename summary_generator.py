def generate_summary(skills, best_role, score):

    if score >= 80:
        level = "strong"

    elif score >= 60:
        level = "good"

    else:
        level = "basic"

    top_skills = ", ".join(skills[:5])

    summary = (
        f"Candidate has {level} technical skills in "
        f"{top_skills}. "
        f"The resume shows potential for "
        f"{best_role} roles with an ATS score of "
        f"{score}%. "
        f"Improving projects, certifications, and "
        f"experience can further strengthen the profile."
    )

    return summary