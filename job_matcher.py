import json

def load_job_roles():
    with open("dataset/job_roles.json", "r") as file:
        roles = json.load(file)
    return roles


def match_jobs(user_skills):
    roles = load_job_roles()
    results = {}

    for role, skills in roles.items():
        matched = set(user_skills) & set(skills)
        missing = set(skills) - set(user_skills)

        score = (len(matched) / len(skills)) * 100

        results[role] = {
            "score": round(score, 2),
            "missing_skills": list(missing)
        }

    return results
