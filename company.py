import streamlit as st
from app.core.db import add_job

def company_page():

    st.header("Company Portal")

    cname = st.text_input("Company Name")
    cemail = st.text_input("Company Email")
    title = st.text_input("Job Title")
    desc = st.text_area("Job Description")

    if st.button("Post Job"):

        add_job(cname, cemail, title, desc)
        st.success("Job Posted ✔️")
