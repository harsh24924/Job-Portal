import json
import numpy
from schemas import Job
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code = True)
data = json.load(open("data/jobs.json"))
jobs = [Job(**item) for item in data]
fields_order = ["title", "company", "location", "description", "requirements"]

all_strings = []
for job in jobs:
    for field in fields_order:
        all_strings.append(getattr(job, field))

task_prefix = "clustering: "
prefixed_strings = [f"{task_prefix}{s}" for s in all_strings]

embeddings_2d = model.encode(prefixed_strings, show_progress_bar = True)

num_jobs = len(jobs)
num_fields = len(fields_order)
embedding_dim = model.get_sentence_embedding_dimension()

assert embedding_dim is not None, "Could not determine the embedding dimension from the model."

embeddings_3d = embeddings_2d.reshape(num_jobs, num_fields, embedding_dim)

print(f"Shape of the final NumPy array: {embeddings_3d.shape}")
print(f"Expected shape: ({num_jobs}, {num_fields}, {embedding_dim})")

numpy.save("data/jobs.npy", embeddings_3d)