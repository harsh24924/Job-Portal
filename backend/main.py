import numpy
import analyze
import schemas
import helpers
import recommend
from typing import List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code = True)

@app.post("/recommend/", response_model = list[schemas.Job])
def get_recommendations(resume: schemas.Resume):
    resume_embeddings = recommend.encode_resume(model, resume.model_dump())
    all_job_embeddings = numpy.load("data/jobs.npy")
    scores = recommend.calculate_scores(resume_embeddings, all_job_embeddings)
    jobs = helpers.load_jobs("data/jobs.json")
    recommended_jobs = recommend.get_recommendations(scores, jobs)
    return recommended_jobs

@app.post("/analyze/", response_model = schemas.Analysis)
def get_analysis(pair: schemas.Pair):
    instructions = open("instructions.txt").read()
    prompt = analyze.prepare_prompt(instructions, pair)
    analysis = analyze.generate(prompt)
    analysis_json = analyze.extract_json(analysis)
    return analysis_json

app.mount("/", StaticFiles(directory = "../frontend", html = True), name = "frontend")