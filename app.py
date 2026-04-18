import streamlit as st

st.title("Resume Recommendation System")

name = st.text_input("Enter your name")
skills = st.text_area("Enter your skills (comma separated)")
experience = st.slider("Experience (years)", 0, 10)
salary = st.number_input("Expected Salary")

if st.button("Recommend"):

    st.write("Hello", name)

    skill_list = skills.lower().split(",")

    if "python" in skill_list:
        st.success("Recommended Role: Python Developer 🐍")

    elif "java" in skill_list:
        st.success("Recommended Role: Java Developer ☕")

    elif experience >= 5:
        st.success("Recommended Role: Senior Developer 👨‍💻")

    else:
        st.info("Recommended Role: Intern / Junior Developer 🚀")