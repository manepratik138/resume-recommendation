import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Internship Portal", layout="wide")

st.title("💼 AI Internship Portal 🤖")

# ---------------- SESSION STORAGE ----------------
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# ---------------- PDF TEXT ----------------
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------- ADD COMPANY / INTERNSHIP ----------------
st.header("➕ Add Company / Internship")

col1, col2 = st.columns(2)

with col1:
    title = st.text_input("Internship Title")
    company = st.text_input("Company Name")

with col2:
    skills = st.text_input("Required Skills (comma separated)")
    location = st.text_input("Location")

if st.button("Add Internship"):

    if title and company:
        st.session_state.jobs.append({
            "title": title,
            "company": company,
            "skills": skills,
            "location": location
        })

        st.success("Internship Added ✔️")

st.markdown("---")

# ---------------- USER RESUME ----------------
st.header("📄 Find Internship Using Resume")

name = st.text_input("Your Name")
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
manual_skills = st.text_area("Or Enter Skills Manually")

resume_text = ""

if file:
    resume_text = extract_text(file)

all_input = (resume_text + " " + manual_skills).lower()

st.markdown("---")

# ---------------- DISPLAY + MATCH ----------------
st.header("🔥 Available Internships")

for job in st.session_state.jobs:

    st.subheader(job["title"])
    st.write("🏢 Company:", job["company"])
    st.write("📍 Location:", job["location"])
    st.write("🧠 Skills:", job["skills"])

    # ---------------- AI MATCH ----------------
    match = False

    for skill in job["skills"].lower().split(","):
        if skill.strip() in all_input:
            match = True

    if match:
        st.success("🔥 MATCH FOUND for you!")
    else:
        st.info("Not a match yet")

    # ---------------- APPLY ----------------
    if st.button(f"Apply - {job['title']}"):
        st.success(f"Application Sent by {name} ✔️")
