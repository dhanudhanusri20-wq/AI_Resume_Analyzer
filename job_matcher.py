def match_jobs(skills):

    job_roles = {

        "Python Developer": [
            "python",
            "sql",
            "flask",
            "django"
        ],

        "Data Scientist": [
            "python",
            "machine learning",
            "data science",
            "power bi",
            "excel"
        ],

        "Frontend Developer": [
            "html",
            "css",
            "javascript",
            "react"
        ],

        "Backend Developer": [
            "python",
            "sql",
            "django",
            "flask"
        ]
    }

    results = {}

    for role, required_skills in job_roles.items():

        matched = []

        missing = []

        for skill in required_skills:

            if skill.lower() in skills:
                matched.append(skill)

            else:
                missing.append(skill)

        score = int((len(matched) / len(required_skills)) * 100)

        results[role] = {
            "score": score,
            "missing_skills": missing
        }

    return results
