import streamlit as st
from app.core.db import get_jobs
from ai.ranker import rank_resume

def jobs_page():

    st.header("Available Jobs")

    jobs = get_jobs()

    for job in jobs:

        st.subheader(job[2])
        st.write(job[3])

        if st.button("Apply", key=job[0]):
            st.success("Applied ✔️")
