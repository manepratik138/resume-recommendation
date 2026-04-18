import streamlit as st

st.set_page_config(page_title="AI Job Portal", layout="wide")

st.title("💼 Dynamic AI Job Portal")

# ---------------- SESSION STORAGE ----------------
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# ---------------- ADD NEW COMPANY ----------------
st.header("➕ Add New Company / Internship")

title = st.text_input("Job Title")
company = st.text_input("Company Name")
skills = st.text_input("Skills Required")
location = st.text_input("Location")

if st.button("Add Job"):

    if title and company:

        st.session_state.jobs.append({
            "title": title,
            "company": company,
            "skills": skills,
            "location": location
        })

        st.success("Job Added Successfully ✔️")

# ---------------- SEARCH ----------------
st.markdown("---")
search = st.text_input("🔍 Search Jobs")

st.markdown("---")

# ---------------- DISPLAY JOBS ----------------
for job in st.session_state.jobs:

    if search.lower() in job["title"].lower() or search == "":

        with st.container():
            st.subheader(job["title"])
            st.write("🏢 Company:", job["company"])
            st.write("📍 Location:", job["location"])
            st.write("🧠 Skills:", job["skills"])

            if st.button(f"Apply {job['title']}"):
                st.success("Application Sent ✔️ (Demo)")

        st.markdown("---")
