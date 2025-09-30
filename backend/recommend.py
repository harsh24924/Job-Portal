import numpy
import helpers

def encode_resume(model, resume):
    categories = list(resume.values())
    prefix = "clustering: "
    sentences = [prefix + item for item in categories]
    embeddings = model.encode(sentences)
    return embeddings

def calculate_scores(resume_embeddings, all_job_embeddings):
    scores = helpers.calculate_scores(resume_embeddings, all_job_embeddings)    
    return scores

def get_recommendations(scores, jobs):
    recommendation_count = 5
    top_indices_ascending = numpy.argsort(scores)[-recommendation_count:]
    recommended_job_indices = top_indices_ascending[::-1]
    recommended_jobs = [jobs[i] for i in recommended_job_indices]
    return recommended_jobs