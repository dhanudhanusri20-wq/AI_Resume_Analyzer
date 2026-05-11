import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from job_matcher import match_jobs
from scoring import calculate_score

# ---------------- PDF GENERATION ---------------- #

def generate_pdf(skills, score, best_role):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=16)

    pdf.cell(
        200,
        10,
        txt="AI Resume Analysis Report",
        ln=True,
        align='C'
    )

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.cell(
        200,
        10,
        txt=f"ATS Resume Score: {score}%",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Best Career Match: {best_role}",
        ln=True
    )

    pdf.ln(10)

    pdf.cell(
        200,
        10,
        txt="Extracted Skills:",
        ln=True
    )

    for skill in skills:

        pdf.cell(
            200,
            10,
            txt=f"- {skill}",
            ln=True
        )

    pdf.output("resume_report.pdf")

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- DARK THEME ---------------- #

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #161B22;
}

h1, h2, h3, h4, h5, h6, p, label, div {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("About")

st.sidebar.info(
    "This AI Resume Analyzer helps evaluate resumes, "
    "analyze skills, calculate ATS scores, and suggest job roles."
)

st.sidebar.markdown("### Features")

st.sidebar.write("✅ Skill Extraction")
st.sidebar.write("✅ ATS Resume Score")
st.sidebar.write("✅ Job Matching")
st.sidebar.write("✅ Missing Skills Detection")
st.sidebar.write("✅ PDF Report Download")

# ---------------- HEADER ---------------- #

st.title("📄 AI Resume Analyzer")

st.markdown("### Get instant career insights from your resume")

st.write(
    "Upload your resume to analyze skills, calculate ATS score, "
    "and get career recommendations."
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ---------------- MAIN APP ---------------- #

if uploaded_file is not None:

    # Extract Resume Text
    text = extract_text_from_pdf(uploaded_file)

    # Loading Spinner
    with st.spinner("Analyzing resume..."):

        # Skill Extraction
        skills = extract_skills(text)

        # ATS Score
        score = calculate_score(text, skills)

        # Job Matching
        job_matches = match_jobs(skills)

    # Empty Skill Check
    if not skills:

        st.error(
            "No relevant skills found. "
            "Please upload a proper resume."
        )

    else:

        # ---------------- SKILLS + SCORE ---------------- #

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🧠 Extracted Skills")

            st.success(" | ".join(skills))

        with col2:

            st.subheader("📊 ATS Resume Score")

            st.progress(score)

            st.success(f"{score}%")

            # Feedback
            if score >= 80:
                st.success("Excellent Resume")

            elif score >= 60:
                st.warning("Good Resume but can improve")

            else:
                st.error("Resume needs improvement")

        # ---------------- JOB MATCH CHART ---------------- #

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

        # ---------------- MISSING SKILLS ---------------- #

        st.markdown("## ⚠️ Missing Skills")

        for role, data in job_matches.items():

            if data['missing_skills']:

                st.warning(
                    f"{role}: "
                    f"{', '.join(data['missing_skills'][:5])}"
                )

        # ---------------- BEST ROLE ---------------- #

        best_role = max(
            job_matches,
            key=lambda x: job_matches[x]['score']
        )

        st.markdown("## 🎯 Best Career Match")

        st.success(
            f"{best_role} "
            f"({job_matches[best_role]['score']}% match)"
        )

        # ---------------- PDF DOWNLOAD ---------------- #

        generate_pdf(skills, score, best_role)

        with open("resume_report.pdf", "rb") as file:

            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )

        # ---------------- SUGGESTIONS ---------------- #

        st.markdown("## 💡 Suggestions")

        for role, data in job_matches.items():

            if data["missing_skills"]:

                st.info(
                    f"For {role}, learn: "
                    f"{', '.join(data['missing_skills'][:5])}"
                )

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption(
    "AI Resume Analyzer | Built using Python, NLP & Streamlit"
)
