from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_summarize_happy_path():
    payload = {"text": "This is a long article ..."}
    resp = client.post("/summarize", json=payload)
    assert resp.status_code == 200
    assert "summary" in resp.json()

def test_summarize_empty_text():
    resp = client.post("/summarize", json={"text": "   "})
    assert resp.status_code == 400
from main import summarize_text, download_nltk_data

def test_nltk_download():
    download_nltk_data()
    assert True

def test_summarize_text():
    text = "This is a test article. It has multiple sentences. We want to summarize it."
    summary = summarize_text(text, 1)
    assert len(summary) > 0
    assert isinstance(summary, str)
