import json
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_recommendations_success():
    resume_data = json.load(open("data/resume.json"))
    response = client.post("/recommend/", json = resume_data)
    assert response.status_code == 200
    assert len(response.json()) == 5
    for job in response.json():
        assert "title" in job
        assert "company" in job
        assert "location" in job
        assert "description" in job
        assert "requirements" in job

def test_recommendation_missing_category():
    resume_data = json.load(open("data/resume.json"))
    del resume_data["summary"]
    response = client.post("/recommend/", json = resume_data)
    assert response.status_code == 422
    assert "summary" in response.json()["detail"][0]["loc"]
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_analysis_success():
    pair_data = json.load(open("data/pair.json"))
    response = client.post("/analyze/", json = pair_data)
    assert response.status_code == 200

def test_analysis_missing_job():
    pair_data = json.load(open("data/pair.json"))
    del pair_data["job"]
    response = client.post("/analyze/", json = pair_data)
    assert response.status_code == 422
    assert "job" in response.json()["detail"][0]["loc"]
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_analysis_missing_resume():
    pair_data = json.load(open("data/pair.json"))
    del pair_data["resume"]
    response = client.post("/analyze/", json = pair_data)
    assert response.status_code == 422
    assert "resume" in response.json()["detail"][0]["loc"]
    assert response.json()["detail"][0]["msg"] == "Field required"
