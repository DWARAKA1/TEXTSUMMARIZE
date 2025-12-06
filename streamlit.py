import logging

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

import streamlit as st
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from transformers import pipeline
from rouge_score import rouge_scorer

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

@st.cache_resource
def load_model():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extractive_summary(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

def abstractive_summary(text):
    summarizer = load_model()
    if len(text) > 1000:
        text = text[:1000]
    summary = summarizer(text, max_length=100, min_length=20, do_sample=False)
    return summary[0]['summary_text']

# ROUGE evaluation function
def get_rouge_scores(reference, generated):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores

# Streamlit UI
st.title("Text Summarization App")

article = st.text_area("Enter the article text:", height=300)
reference_summary = st.text_area("Enter the reference summary (optional, for ROUGE evaluation):", height=100)

summ_type = st.radio("Choose summarization type:", ("Extractive", "Abstractive"))

if st.button("Summarize"):
    if not article.strip():
        st.warning("Please enter article text.")
    else:
        if summ_type == "Extractive":
            summary = extractive_summary(article)
        else:
            summary = abstractive_summary(article)
        st.subheader("Generated Summary")
        st.write(summary)
        
        if reference_summary.strip():
            scores = get_rouge_scores(reference_summary, summary)
            st.subheader("ROUGE Scores")
            for k, v in scores.items():
                st.write(f"{k}: F1={v.fmeasure:.3f}, Precision={v.precision:.3f}, Recall={v.recall:.3f}")

st.markdown("---")
st.caption("Powered by Sumy, HuggingFace Transformers, and ROUGE Score")
