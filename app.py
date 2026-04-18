import streamlit as st

st.title("AI Resume Recommendation System 🤖")

name = st.text_input("Enter your name")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

skills = st.text_area("Or enter your skills manually (comma separated)")
experience = st.slider("Experience (years)", 0, 10)

if st.button("Analyze Resume"):

    st.write("Hello", name)

    skill_list = skills.lower().split(",")

    if "python" in skill_list and experience >= 2:
        st.success("Recommended Role: Data Scientist / Python Developer 🐍")

    elif "java" in skill_list:
        st.success("Recommended Role: Backend Developer ☕")

    elif "html" in skill_list or "css" in skill_list:
        st.success("Recommended Role: Frontend Developer 🎨")

    else:
        st.info("Recommended Role: Intern / Learning Stage 🚀")
