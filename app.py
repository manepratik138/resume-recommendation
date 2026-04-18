import streamlit as st
import sqlite3
import PyPDF2
from datetime import datetime

st.set_page_config(page_title="HireAI SaaS", layout="wide")

st.title("🚀 HireAI - Startup Job Portal")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("startup.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT,
    skills TEXT,
    resume TEXT,
    score INTEGER,
    time TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    title TEXT,
    skills TEXT,
    location TEXT
)''')

conn.commit()

# ---------------- PDF ----------------
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------- AI ----------------
def get_role(text):
    if "python" in text:
        return "Data Scientist"
    elif "html" in text or "css" in text:
        return "Frontend Developer"
    elif "java" in text:
        return "Backend Developer"
    else:
        return "Intern"

def get_score(text):
    score = 0
    keywords = {
        "python": 30,
        "machine learning": 40,
        "html": 15,
        "css": 15,
        "java": 25
    }

    for k, v in keywords.items():
        if k in text:
            score += v

    return min(score, 100)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["👨‍🎓 Student", "🏢 Company", "💼 Jobs"])

# ================= STUDENT =================
with tab1:

    st.header("Student Signup / Apply")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    skills = st.text_area("Skills")
    file = st.file_uploader("Upload Resume", type=["pdf"])

    resume_text = ""
    if file:
        resume_text = extract_text(file)

    full_text = (skills + " " + resume_text).lower()

    if st.button("Register / Apply"):

        role = get_role(full_text)
        score = get_score(full_text)

        time_now = str(datetime.now())

        c.execute("""INSERT INTO users 
        (type, name, email, password, role, skills, resume, score, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("student", name, email, password, role, skills, resume_text, score, time_now))

        conn.commit()

        st.success(f"Registered ✔️ Role: {role} Score: {score}")

# ================= COMPANY =================
with tab2:

    st.header("Company Dashboard")

    cname = st.text_input("Company Name")

    title = st.text_input("Job Title")
    jskills = st.text_input("Required Skills")
    location = st.text_input("Location")

    if st.button("Post Job"):

        c.execute("INSERT INTO jobs (company, title, skills, location) VALUES (?, ?, ?, ?)",
                  (cname, title, jskills, location))

        conn.commit()

        st.success("Job Posted ✔️")

    st.subheader("Applicants")

    c.execute("SELECT name, email, role, skills, score FROM users WHERE type='student' ORDER BY score DESC")
    data = c.fetchall()

    for row in data:
        st.write("👤", row[0], "|", row[1], "|", row[2], "| Score:", row[4])
        st.markdown("---")

# ================= JOBS =================
with tab3:

    st.header("Available Jobs")

    c.execute("SELECT company, title, skills, location FROM jobs")
    jobs = c.fetchall()

    for job in jobs:
        st.subheader(job[1])
        st.write("🏢", job[0])
        st.write("🧠 Skills:", job[2])
        st.write("📍", job[3])

        if st.button(f"Apply {job[1]}"):
            st.success("Application Sent ✔️ (Demo)")
