import json
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_recommendations_success():
    resume_data = json.load(open("data/resume.json"))
    response = client.post("/recommend/", json = resume_data)
    assert response.status_code == 200

def test_get_analysis_success():
    pair_data = json.load(open("data/pair.json"))
    response = client.post("/analyze/", json = pair_data)
    print(response.json())
    assert response.status_code == 200