def extract_skills(text):

    skills_list = [
        "python",
        "java",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "sql",
        "machine learning",
        "data science",
        "react",
        "node js",
        "django",
        "flask",
        "power bi",
        "excel",
        "communication",
        "leadership",
        "teamwork"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills
