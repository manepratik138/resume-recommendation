import streamlit as st

st.set_page_config(page_title="AI Hiring SaaS", layout="wide")

st.title("💼 AI Hiring SaaS 🚀")

tab1, tab2, tab3 = st.tabs(["👨‍🎓 Student", "🏢 Company", "💼 Jobs"])

with tab1:
    from app.pages.student import student_page
    student_page()

with tab2:
    from app.pages.company import company_page
    company_page()

with tab3:
    from app.pages.jobs import jobs_page
    jobs_page()
