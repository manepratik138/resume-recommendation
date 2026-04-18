import streamlit as st
import sqlite3

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

def get_jobs():
    return c.execute("SELECT * FROM jobs").fetchall()

def get_users():
    return c.execute("SELECT * FROM users").fetchall()

# ---------------- UI ----------------
st.set_page_config(page_title="AI Hiring SaaS", layout="wide")

st.title("💼 AI Hiring SaaS 🚀")

menu = st.sidebar.selectbox("Menu", ["Student Apply", "Company Post", "Jobs", "Admin Panel"])

# ---------------- STUDENT ----------------
if menu == "Student Apply":

    st.header("👨‍🎓 Student Apply")

    name = st.text_input("Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills")

    if st.button("Apply"):
        add_user(name, email, skills)
        st.success("Applied Successfully ✔️")

# ---------------- COMPANY ----------------
elif menu == "Company Post":

    st.header("🏢 Company Job Post")

    company = st.text_input("Company Name")
    email = st.text_input("Company Email")
    title = st.text_input("Job Title")
    desc = st.text_area("Job Description")

    if st.button("Post Job"):
        add_job(company, email, title, desc)
        st.success("Job Posted ✔️")

# ---------------- JOBS ----------------
elif menu == "Jobs":

    st.header("💼 Available Jobs")

    jobs = get_jobs()

    for job in jobs:
        st.subheader(job[3])
        st.write(job[4])
        st.markdown("---")

# ---------------- ADMIN ----------------
elif menu == "Admin Panel":

    st.header("🛠️ Admin Dashboard")

    users = get_users()
    jobs = get_jobs()

    st.metric("Total Students", len(users))
    st.metric("Total Jobs", len(jobs))

    st.subheader("👨‍🎓 Students")
    for u in users:
        st.write(u)

    st.subheader("🏢 Jobs")
    for j in jobs:
        st.write(j)
