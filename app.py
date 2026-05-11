import streamlit as st
import pandas as pd
import base64
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from job_matcher import match_jobs
from scoring import calculate_score

# 🔥 Background Image Function
def set_bg_image():
    with open("assets/bg.jpg", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 12px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🔥 Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Apply background
set_bg_image()

# 🔥 Sidebar
st.sidebar.title("About")
st.sidebar.info(
    "This AI Resume Analyzer helps you evaluate your resume, "
    "match job roles, and identify missing skills."
)

st.sidebar.markdown("### Features")
st.sidebar.write("- Skill Extraction")
st.sidebar.write("- Job Matching")
st.sidebar.write("- Resume Scoring")
st.sidebar.write("- Career Suggestions")

# 🔥 Header
st.title("📄 AI Resume Analyzer")
st.markdown("### Get instant career insights from your resume")
st.write("Upload your resume to analyze skills, match job roles, and get improvement suggestions.")

# 🔥 Upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Extract text
    text = extract_text_from_pdf(uploaded_file)

    # Loading effect
    with st.spinner("Analyzing resume..."):
        skills = extract_skills(text)
        score = calculate_score(text, skills)
        job_matches = match_jobs(skills)

    # Handle empty case
    if not skills:
        st.error("No relevant skills found. Please upload a proper resume.")
    else:
        # 🔹 Skills & Score
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧠 Extracted Skills")
            st.success(" | ".join(skills))

        with col2:
            st.subheader("📊 Resume Score")
            st.metric(label="Score", value=f"{score}%")

        # 🔹 Chart
        st.markdown("## 📊 Job Match Analysis")

        roles = []
        scores = []

        for role, data in job_matches.items():
            roles.append(role)
            scores.append(data['score'])

        df = pd.DataFrame({
            "Role": roles,
            "Match %": scores
        })

        st.bar_chart(df.set_index("Role"))

        # 🔹 Missing Skills
        st.markdown("## ⚠️ Missing Skills")

        for role, data in job_matches.items():
            if data['missing_skills']:
                st.warning(f"{role}: {', '.join(data['missing_skills'][:5])}")

        # 🔹 Best Role
        best_role = max(job_matches, key=lambda x: job_matches[x]['score'])
        st.markdown("## 🎯 Best Career Match")
        st.success(f"{best_role} ({job_matches[best_role]['score']}% match)")

        # 🔹 Suggestions
        st.markdown("## 💡 Suggestions")

        for role, data in job_matches.items():
            if data["missing_skills"]:
                st.info(f"For {role}, learn: {', '.join(data['missing_skills'][:5])}")

# 🔥 Footer
st.markdown("---")
st.caption("AI Resume Analyzer | Built with Python, NLP & Streamlit")

