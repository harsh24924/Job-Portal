from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: str

class Resume(BaseModel):
    summary: str
    skills: str
    education: str
    experience: str
    projects: str

class Analysis(BaseModel):
    matches: list[str]
    missing: list[str]

class Pair(BaseModel):
    job: Job
    resume: Resume