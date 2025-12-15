from fastapi import FastAPI
from models import Developer, Project

app = FastAPI()

@app.post("/developers/")
def create_developer(developer: Developer):
    return {"message":"Developer created successfully","developer":developer}

@app.post("/projects/")
def create_projects(project: Project):
    return{"message":"project created successfully","project": project}

@app.get("/projects/")
def get_projects():
    sample_project = Project(
        title="Sample Project",
        description="This is a sample project",
        languages = ["Python","JavaScript"],
        lead_developer = Developer(name="John doe", experience=5)
    )
    return{"projects",[sample_project]}

