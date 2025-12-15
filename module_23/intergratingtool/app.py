import streamlit as st
import requests
import pandas as pd


st.title('Project Management App')


st.header("Add a Developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input("Experience (Years)", min_value=0, max_value=50, value=0)

if st.button("Create Developer"):
    dev_data = {'name': dev_name, 'experience': dev_experience}
    dev_response = requests.post(url="http://localhost:8000/developers/", json=dev_data)
    st.json(dev_response.json())


st.header("Add a Project")
proj_title = st.text_input("Project Title")
proj_desc = st.text_area("Project Description")
proj_langs = st.text_input("Languages Used (Comma-separated)")
lead_dev_name = st.text_input("Lead Developer Name")
lead_dev_exp = st.number_input("Lead Developer Experience (Years)", min_value=0, max_value=50, value=0)

if st.button("Create Project"):
    lead_dev_data = {"name": lead_dev_name, "experience": lead_dev_exp}
    proj_data = {
        "title": proj_title,
        "description": proj_desc,
        "languages": proj_langs.split(','),
        "lead_developer": lead_dev_data
    }
    proj_response = requests.post("http://localhost:8000/projects/", json=proj_data)
    st.json(proj_response.json())


st.header("Project Dashboard")

if st.button("Get Projects"):
    project_response = requests.get("http://localhost:8000/projects/")
    projects_data = project_response.json().get('projects', [])

    if projects_data:
        projects_df = pd.DataFrame(projects_data)
        st.subheader("Projects Overview")
        st.dataframe(projects_df)

        st.subheader("Project Details")
        for project in projects_df.to_dict(orient="records"):
            st.markdown(f"**Title:** {project['title']}")
            st.markdown(f"**Description:** {project['description']}")
            st.markdown(f"**Languages:** {', '.join(project['languages'])}")
            st.markdown(f"**Lead Developer:** {project['lead_developer']['name']} with {project['lead_developer']['experience']} years of experience")
            st.markdown("---")
    else:
        st.warning("No projects found.")
