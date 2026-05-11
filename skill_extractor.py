import json

def load_skills():
    with open("dataset/skills.json", "r") as file:
        skills = json.load(file)
    return skills

def extract_skills(text):
    skills_list = load_skills()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
