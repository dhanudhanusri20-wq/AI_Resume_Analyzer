def calculate_score(skills):
    base = len(skills) * 8

    if "python" in skills:
        base += 10
    if "machine learning" in skills:
        base += 10

    if base > 100:
        base = 100

    return base
