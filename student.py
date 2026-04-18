import streamlit as st
from app.core.db import add_user

def student_page():

    st.header("Student Apply")

    name = st.text_input("Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills")

    if st.button("Apply"):

        add_user(name, email, skills)
        st.success("Applied ✔️")
