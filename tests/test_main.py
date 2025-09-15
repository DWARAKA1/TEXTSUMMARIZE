from main import summarize_text, download_nltk_data

def test_nltk_download():
    download_nltk_data()
    assert True

def test_summarize_text():
    text = "This is a test article. It has multiple sentences. We want to summarize it."
    summary = summarize_text(text, 1)
    assert len(summary) > 0
    assert isinstance(summary, str)