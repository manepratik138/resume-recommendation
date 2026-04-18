import streamlit as st
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- DATABASE ----------------
conn = sqlite3.connect("saas.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    skills TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    email TEXT,
    title TEXT,
    description TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    skills TEXT,
    job_title TEXT,
    score REAL
)''')

conn.commit()

# ---------------- FUNCTIONS ----------------
def add_user(name, email, skills):
    c.execute("INSERT INTO users (name,email,skills) VALUES (?,?,?)",
              (name, email, skills))
    conn.commit()

def add_job(company, email, title, desc):
    c.execute("INSERT INTO jobs (company,email,title,description) VALUES (?,?,?,?)",
              (company, email, title, desc))
    conn.commit()

def get_users():
    return c.execute("SELECT * FROM users").fetchall()

def get_jobs():
    return c.execute("SELECT * FROM jobs").fetchall()

# ---------------- AI RANKING ----------------
def get_match_score(resume, job):

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([resume, job])

    score = cosine_similarity(matrix[0], matrix[1])[0][0]

    return round(score * 100, 2)

# ---------------- UI ----------------
st.set_page_config(page_title="AI Hiring SaaS", layout="wide")

st.title("💼 AI Hiring SaaS 🚀")

menu = st.sidebar.selectbox(
    "Menu",
    ["Student Apply", "Company Post", "Jobs", "Admin Dashboard"]
)

# ---------------- STUDENT APPLY ----------------
if menu == "Student Apply":

    st.header("👨‍🎓 Student Apply")

    name = st.text_input("Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills / Resume Text")

    jobs = get_jobs()
    job_titles = [j[3] for j in jobs]

    selected_job = st.selectbox("Select Job", job_titles)

    if st.button("Apply & Get AI Score"):

        job_desc = ""
        for j in jobs:
            if j[3] == selected_job:
                job_desc = j[4]

        score = get_match_score(skills, job_desc)

        c.execute("INSERT INTO applications VALUES (NULL,?,?,?,?,?)",
                  (name, email, skills, selected_job, score))
        conn.commit()

        st.success(f"Applied Successfully ✔️ Match Score: {score}%")

# ---------------- COMPANY POST ----------------
elif menu == "Company Post":

    st.header("🏢 Post Job")

    company = st.text_input("Company Name")
    email = st.text_input("Company Email")
    title = st.text_input("Job Title")
    desc = st.text_area("Job Description")

    if st.button("Post Job"):
        add_job(company, email, title, desc)
        st.success("Job Posted ✔️")

# ---------------- JOB LIST ----------------
elif menu == "Jobs":

    st.header("💼 Jobs")

    jobs = get_jobs()

    for job in jobs:
        st.subheader(job[3])
        st.write(job[4])
        st.markdown("---")

# ---------------- ADMIN DASHBOARD ----------------
elif menu == "Admin Dashboard":

    st.header("🛠️ Admin Dashboard (AI Ranking)")

    users = get_users()
    jobs = get_jobs()

    st.metric("Total Students", len(users))
    st.metric("Total Jobs", len(jobs))

    st.subheader("🏆 AI Ranked Candidates")

    if len(jobs) > 0 and len(users) > 0:

        job_desc = jobs[0][4]

        ranked = []

        for u in users:
            score = get_match_score(u[3], job_desc)
            ranked.append((u[1], u[2], u[3], score))

        ranked.sort(key=lambda x: x[3], reverse=True)

        for r in ranked:

            st.write("👤 Name:", r[0])
            st.write("📧 Email:", r[1])
            st.write("🧠 Skills:", r[2])
            st.write("📊 Score:", r[3], "%")
            st.markdown("---")
