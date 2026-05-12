import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from job_matcher import match_jobs
from scoring import calculate_score
from career_advisor import get_career_advice

# ---------------- BACKGROUND ---------------- #

def set_bg():
    try:
        with open("assets/bg.jpg", "rb") as file:
            data = file.read()

        encoded = base64.b64encode(data).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        section[data-testid="stSidebar"] {{
            background-color: rgba(0,0,0,0.7);
        }}
        h1,h2,h3,h4,h5,h6,p,div,label {{
            color: white;
        }}
        </style>
        """, unsafe_allow_html=True)

    except:
        st.markdown("""
        <style>
        .stApp { background-color:#0E1117; color:white; }
        section[data-testid="stSidebar"] { background-color:#161B22; }
        h1,h2,h3,h4,h5,h6,p,div,label { color:white; }
        </style>
        """, unsafe_allow_html=True)

# ---------------- LOGIN ---------------- #

def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- SCORE BREAKDOWN ---------------- #

def score_breakdown(text, skills, job_matches):

    skill_score = min(len(skills) * 4, 40)
    ats_score = min(calculate_score(text, skills), 30)

    best_match_score = max(
        [job_matches[j]["score"] for j in job_matches]
    ) if job_matches else 0

    job_score = best_match_score * 0.2

    structure_keywords = ["education", "experience", "project", "skills"]
    structure_score = sum(2.5 for k in structure_keywords if k in text.lower())

    total = skill_score + ats_score + job_score + structure_score

    return {
        "Skill Score": round(skill_score, 2),
        "ATS Score": round(ats_score, 2),
        "Job Match Score": round(job_score, 2),
        "Structure Score": round(structure_score, 2),
        "Total Score": round(total, 2)
    }

# ---------------- TIPS GENERATOR ---------------- #

def generate_resume_tips(text, skills, score):

    tips = []

    if len(skills) < 5:
        tips.append("Add more technical skills like Python, SQL, ML")

    if "project" not in text.lower():
        tips.append("Add a Projects section")

    if "experience" not in text.lower():
        tips.append("Include internship or experience details")

    if score < 60:
        tips.append("ATS score is low — improve keyword usage")

    elif score < 80:
        tips.append("Good resume but needs optimization")

    else:
        tips.append("Strong resume — tailor for each job")

    tips.append("Use action verbs: built, developed, designed, implemented")

    return tips

# ---------------- PDF ---------------- #

def generate_pdf(skills, score, best_role):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 16)
    pdf.cell(200, 10, "AI Resume Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 12)
    pdf.cell(200, 10, f"Score: {score}%", ln=True)
    pdf.cell(200, 10, f"Best Role: {best_role}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, "Skills:", ln=True)

    for s in skills:
        pdf.cell(200, 10, f"- {s}", ln=True)

    pdf.output("report.pdf")

# ---------------- CONFIG ---------------- #

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
set_bg()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Menu")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.info("AI Resume Analyzer System")

# ---------------- MAIN ---------------- #

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Analyzing..."):

        skills = extract_skills(text)
        score = calculate_score(text, skills)
        job_matches = match_jobs(skills)

    if not skills:
        st.error("No skills found")
        st.stop()

    best_role = max(job_matches, key=lambda x: job_matches[x]["score"])

    tab1, tab2, tab3, tab4 = st.tabs([
        "Dashboard", "Charts", "Analysis", "Career Advice"
    ])

    # ---------------- DASHBOARD ---------------- #
    with tab1:

        st.subheader("Skills")
        st.success(" | ".join(skills))

        st.markdown("## Score Breakdown")

        breakdown = score_breakdown(text, skills, job_matches)

        dfb = pd.DataFrame({
            "Category": breakdown.keys(),
            "Score": breakdown.values()
        })

        st.bar_chart(dfb.set_index("Category"))

        st.markdown("## Metrics")
        c1, c2, c3 = st.columns(3)

        c1.metric("ATS Score", f"{score}%")
        c2.metric("Skills", len(skills))
        c3.metric("Best Match", best_role)

    # ---------------- CHARTS ---------------- #
    with tab2:

        roles = list(job_matches.keys())
        scores = [job_matches[r]["score"] for r in roles]

        df = pd.DataFrame({"Role": roles, "Score": scores})
        st.bar_chart(df.set_index("Role"))

        fig, ax = plt.subplots()
        ax.pie(scores, labels=roles, autopct="%1.1f%%")
        st.pyplot(fig)

    # ---------------- ANALYSIS ---------------- #
    with tab3:

        st.markdown("## Missing Skills")

        for role, data in job_matches.items():
            if data["missing_skills"]:
                st.warning(f"{role}: {', '.join(data['missing_skills'][:5])}")

        st.markdown("## Resume Sections")

        sections = {
            "Education": ["education"],
            "Skills": ["skills"],
            "Projects": ["project"],
            "Experience": ["experience"]
        }

        for sec, keys in sections.items():
            if any(k in text.lower() for k in keys):
                st.success(f"{sec} found")
            else:
                st.error(f"{sec} missing")

    # ---------------- CAREER ---------------- #
    with tab4:

        st.markdown("## Career Advice")
        st.info(get_career_advice(best_role))

        st.markdown("## Resume Tips")

        tips = generate_resume_tips(text, skills, score)

        for t in tips:
            st.warning(t)

        generate_pdf(skills, score, best_role)

        with open("report.pdf", "rb") as f:
            st.download_button("Download Report", f, "resume.pdf")

# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("AI Resume Analyzer | Streamlit + NLP Project")
