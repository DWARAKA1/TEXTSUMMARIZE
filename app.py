from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from config import Settings
from main import summarize_text  # adapt to your actual function

settings = Settings()
app = FastAPI(title="Text Summarization API")

class SummarizeRequest(BaseModel):
    text: str
    max_sentences: int | None = None

class SummarizeResponse(BaseModel):
    summary: str

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Input text is empty")
    summary = summarize_text(req.text, max_sentences=req.max_sentences)
    return SummarizeResponse(summary=summary)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.port, reload=True)
