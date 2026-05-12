def get_career_advice(role):

    advice = {

        "Python Developer":
        """
        Learn Django, Flask, APIs, and SQL.
        Build backend projects and deploy applications.
        """,

        "Data Scientist":
        """
        Focus on Machine Learning, Pandas, NumPy,
        Data Visualization, and Deep Learning.
        """,

        "Frontend Developer":
        """
        Improve React, JavaScript, UI/UX,
        responsive design, and frontend frameworks.
        """,

        "Backend Developer":
        """
        Learn APIs, databases, authentication,
        cloud deployment, and backend frameworks.
        """
    }

    return advice.get(
        role,
        "Keep improving technical and communication skills."
    )