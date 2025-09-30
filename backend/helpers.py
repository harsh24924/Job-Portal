import json
import numpy
from schemas import Job

def calculate_scores(resume_embeddings, job_embeddings):
    resume_norm = numpy.linalg.norm(resume_embeddings, axis = 1, keepdims = True)
    resume_normalized = resume_embeddings / (resume_norm + 1e-8)

    job_norm = numpy.linalg.norm(job_embeddings, axis=2, keepdims = True)
    job_normalized = job_embeddings / (job_norm + 1e-8)

    similarity_matrix = numpy.einsum("ij,klj->kil", resume_normalized, job_normalized)
    max_similarities = numpy.max(similarity_matrix, axis = 2)
    scores = numpy.sum(max_similarities, axis = 1)
    return scores

def load_jobs(file_path):
    data = json.load(open("data/jobs.json"))

    jobs = []
    for item in data:
        job = Job(**item)
        jobs.append(job.model_dump()) 

    return jobs