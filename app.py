import streamlit as st
import sqlite3
import PyPDF2
import smtplib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

st.set_page_config(page_title="AI Hiring SaaS", layout="wide")

st.title("💼 AI Resume + Job Portal SaaS 🚀")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("ai_saas.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    skills TEXT,
    resume TEXT,
    time TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    email TEXT,
    title TEXT,
    description TEXT
)''')

conn.commit()

# ---------------- EMAIL ----------------
def send_email(to_email, subject, message):

    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, msg)
        server.quit()

    except Exception as e:
        st.warning(f"Email failed: {e}")

# ---------------- PDF ----------------
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------- AI MODEL ----------------
def rank_resume(resume_text, job_desc):

    if not resume_text or not job_desc:
        return 0

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc])

    score = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(score * 100, 2)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["👨‍🎓 Student", "🏢 Company"])

# ================= STUDENT =================
with tab1:

    st.header("Student Apply")

    name = st.text_input("Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills")
    file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    resume_text = ""
    if file:
        resume_text = extract_text(file)

    if st.button("Apply Now"):

        time_now = str(datetime.now())

        c.execute("INSERT INTO users (name, email, skills, resume, time) VALUES (?, ?, ?, ?, ?)",
                  (name, email, skills, resume_text, time_now))

        conn.commit()

        st.success("Applied Successfully ✔️")

# ================= COMPANY =================
with tab2:

    st.header("Company Dashboard")

    cname = st.text_input("Company Name")
    cemail = st.text_input("Company Email")

    title = st.text_input("Job Title")
    desc = st.text_area("Job Description")

    if st.button("Post Job"):

        c.execute("INSERT INTO jobs (company, email, title, description) VALUES (?, ?, ?, ?)",
                  (cname, cemail, title, desc))

        conn.commit()

        st.success("Job Posted ✔️")

        # ---------------- GET USERS ----------------
        c.execute("SELECT name, email, resume FROM users")
        users = c.fetchall()

        ranked = []

        for u in users:
            score = rank_resume(u[2], desc)
            ranked.append((u[0], u[1], score))

        ranked.sort(key=lambda x: x[2], reverse=True)

        if ranked:

            top = ranked[0]

            # EMAIL TO COMPANY
            send_email(
                cemail,
                "🎯 Best Candidate Found",
                f"""
Best Candidate:

Name: {top[0]}
Email: {top[1]}
Match Score: {top[2]}%

Job: {title}
"""
            )

            # EMAIL TO TOP STUDENT
            if top[2] > 70:

                send_email(
                    top[1],
                    "🎉 You are Shortlisted!",
                    f"""
Congratulations {top[0]}!

You are shortlisted for:
{title}

Match Score: {top[2]}%

- AI Hiring System
"""
                )

        st.success("Ranking + Emails Sent ✔️")

    # ---------------- SHOW RANKING ----------------
    st.subheader("Candidate Ranking")

    c.execute("SELECT name, email, resume FROM users")
    users = c.fetchall()

    for u in users:

        score = rank_resume(u[2], desc)

        st.write("👤", u[0])
        st.write("📧", u[1])
        st.write("⭐ Match Score:", score, "%")
        st.markdown("---")
