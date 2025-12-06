# TextSummarize

**End-to-End Text Summarization Platform with FastAPI, Streamlit, Docker & Jenkins CI/CD**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

TextSummarize is a production-ready text summarization platform that combines **extractive** and **abstractive** summarization techniques. It provides multiple interfaces (CLI, REST API, and Streamlit UI) for different use cases, with full containerization and CI/CD pipeline support.

## Architecture

```
Request Flow:
├── Input Sources
│   ├── CLI (main.py)
│   ├── REST API (app.py - FastAPI)
│   └── Web UI (streamlit.py)
├── Preprocessing
│   └── Text validation, cleaning, tokenization
├── Summarization Engines
│   ├── Extractive (Sumy - LexRank)
│   └── Abstractive (Transformers - BART)
├── Post-processing
│   └── Output formatting, ROUGE metrics
└── Response
    ├── JSON (API)
    ├── CLI Output
    └── Web Display
```

## Features

- **Dual Summarization Methods**
  - Extractive summarization using Sumy (LexRank algorithm)
  - Abstractive summarization using Transformers (BART model)

- **Multiple Interfaces**
  - REST API with FastAPI for service integration
  - Streamlit web UI for interactive demos
  - CLI for batch processing

- **Production-Grade**
  - Structured logging with JSON format
  - Health checks and metrics endpoints
  - Comprehensive error handling
  - Environment-based configuration

- **Evaluation & Monitoring**
  - ROUGE metrics for summarization quality
  - Request logging and performance tracking
  - Model performance monitoring

- **DevOps Ready**
  - Docker containerization
  - Jenkins CI/CD pipeline (lint → test → build → deploy)
  - Unit and integration tests
  - Automated dependency management

## Tech Stack

| Component | Technology |
|-----------|------------|
| API | FastAPI, Uvicorn |
| UI | Streamlit |
| ML | Transformers, Sumy, PyTorch |
| Testing | Pytest, FastAPI TestClient |
| Linting | Ruff, Black |
| Containerization | Docker |
| CI/CD | Jenkins |
| Config Management | Pydantic, dotenv |
| Logging | Python logging, JSON format |

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or uv (recommended)
- Docker (optional, for containerized deployment)

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/DWARAKA1/TEXTSUMMARIZE.git
cd TEXTSUMMARIZE

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional, uses defaults if not provided)
cp .env.example .env
```

### Docker Setup

```bash
# Build Docker image
docker build -t textsummarize:latest .

# Run container
docker run -p 8000:8000 -e ENV=production textsummarize:latest
```

## Usage

### 1. REST API (Production Recommended)

```bash
# Start FastAPI server
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Example API Requests:**

```bash
# Health check
curl http://localhost:8000/health

# Summarize text
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long article text here...",
    "max_sentences": 3
  }'

Response:
{
  "summary": "Short summary of the text..."
}
```

API Documentation: http://localhost:8000/docs (Swagger UI)

### 2. Web Interface (Interactive Demo)

```bash
streamlit run streamlit.py
```

Access at: http://localhost:8501

### 3. Command Line

```bash
# Basic usage
python main.py

# With custom parameters
python main.py --method extractive --num_sentences 5
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# Environment
ENV=production

# Model Configuration
MODEL_NAME=facebook/bart-large-cnn
MAX_INPUT_TOKENS=2048
DEVICE=cpu  # or 'cuda' for GPU

# API Configuration
PORT=8000
LOG_LEVEL=INFO

# Summarization
DEFAULT_NUM_SENTENCES=3
MIN_TEXT_LENGTH=50
MAX_TEXT_LENGTH=50000

# Performance
ENABLE_CACHE=True
CACHE_EXPIRY=3600
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

## CI/CD Pipeline

### Jenkins Stages

1. **Lint**: Code quality checks with Ruff and Black
2. **Test**: Unit and integration tests with Pytest
3. **Build**: Docker image creation
4. **Deploy**: Push to registry and deploy to target environment

### GitHub Actions (Alternative)

See `.github/workflows/` for GitHub Actions CI/CD configuration.

## Deployment

### Production on EC2/VPS

```bash
# SSH to server
ssh -i key.pem ec2-user@your-instance

# Pull latest image
docker pull your-registry/textsummarize:latest

# Run with environment config
docker run -d \
  -p 8000:8000 \
  -e ENV=production \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  --name textsummarize \
  your-registry/textsummarize:latest
```

### Kubernetes Deployment

See `k8s/deployment.yaml` for Kubernetes manifests.

## Monitoring & Logging

### Health Check

```bash
curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker logs textsummarize -f

# Local logs
tail -f logs/TextSummarize.log
```

### Metrics

Structured logging captures:
- Request latency
- Error rates
- Model inference time
- Cache hit rates

## Project Structure

```
TEXTSUMMARIZE/
├── app.py                   # FastAPI REST API
├── main.py                  # CLI entry point
├── streamlit.py             # Streamlit UI
├── config.py                # Configuration management
├── health_check.py          # Health check utilities
├── Dockerfile               # Container definition
├── Jenkinsfile              # CI/CD pipeline
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
├── pyproject.toml           # Project metadata
├── .env.example             # Environment template
├── tests/
│   ├── test_api.py          # API tests
│   ├── test_main.py         # Core logic tests
│   └── test_config.py       # Configuration tests
├── logs/                    # Application logs
└── README.md                # This file
```

## Performance Tuning

### API Response Times
- **Extractive**: ~500ms (no model loading needed)
- **Abstractive**: ~2-5s (depends on text length and hardware)

### Optimization Tips
1. Use GPU (`DEVICE=cuda`) for faster inference
2. Enable caching for repeated requests
3. Adjust `MAX_INPUT_TOKENS` based on memory
4. Use connection pooling for database calls

## Troubleshooting

### Out of Memory Error
```bash
# Reduce batch size or max tokens
export MAX_INPUT_TOKENS=1024
export DEVICE=cpu  # Fall back to CPU
```

### Slow API Response
```bash
# Enable GPU support
export DEVICE=cuda

# Check logs for bottlenecks
tail -f logs/TextSummarize.log | grep "duration"
```

### Model Download Issues
```bash
# Pre-download model
python -c "from transformers import AutoModelForSeq2SeqLM; AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large-cnn')"
```

## Development

### Code Style

```bash
# Format code
black .

# Lint code
ruff check . --fix
```

### Adding New Features

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run `pytest` to ensure tests pass
4. Submit a pull request

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Roadmap

- [ ] Support for multi-language summarization
- [ ] Fine-tuned models for domain-specific content
- [ ] Real-time streaming summarization
- [ ] Kubernetes deployment templates
- [ ] GraphQL API support
- [ ] Web UI enhancements (dark mode, export options)

## License

MIT License - see LICENSE file for details

## Authors

- **DWARAKA1** - Initial development

## Support

For issues, questions, or suggestions:
- Create an [Issue](https://github.com/DWARAKA1/TEXTSUMMARIZE/issues)
- Check [Discussions](https://github.com/DWARAKA1/TEXTSUMMARIZE/discussions)
- Email: support@textsummarize.dev

## Acknowledgments

- [Transformers](https://huggingface.co/transformers/) by Hugging Face
- [Sumy](https://github.com/MhleCoder/sumy) for extractive summarization
- [FastAPI](https://fastapi.tiangolo.com/) for the REST framework
- [Streamlit](https://streamlit.io/) for the web interface

---

**Last Updated**: December 2025  
**Version**: 1.0.0 (Production Ready)
