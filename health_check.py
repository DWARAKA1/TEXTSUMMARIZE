#!/usr/bin/env python
"""
Health check script for TextSummarize application.
Verifies that all dependencies are properly installed and accessible.
"""

import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required dependencies are installed."""
    dependencies = {
        'nltk': 'Natural Language Toolkit',
        'sumy': 'Sumy summarization library',
        'transformers': 'HuggingFace Transformers',
        'torch': 'PyTorch',
        'streamlit': 'Streamlit web framework',
        'datasets': 'HuggingFace Datasets',
        'rouge_score': 'ROUGE scoring',
    }
    
    all_ok = True
    for module_name, description in dependencies.items():
        try:
            __import__(module_name.replace('-', '_'))
            logger.info(f"✓ {description} ({module_name}) - OK")
        except ImportError as e:
            logger.error(f"✗ {description} ({module_name}) - FAILED: {e}")
            all_ok = False
    
    return all_ok


def check_nltk_data():
    """Check if NLTK data is available."""
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        logger.info("✓ NLTK tokenizers data - OK")
        return True
    except LookupError:
        logger.warning("⚠ NLTK data not found. Run: nltk.download('punkt')")
        return False


def check_application_files():
    """Check if required application files exist."""
    import os
    
    required_files = [
        'main.py',
        'streamlit.py',
        'requirements.txt',
        'tests/test_main.py'
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            logger.info(f"✓ {file_path} - Found")
        else:
            logger.error(f"✗ {file_path} - NOT FOUND")
            all_ok = False
    
    return all_ok


def main():
    """Run all health checks."""
    logger.info("Starting TextSummarize health check...")
    logger.info("=" * 50)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("NLTK Data", check_nltk_data),
        ("Application Files", check_application_files),
    ]
    
    results = []
    for check_name, check_func in checks:
        logger.info(f"\nChecking {check_name}...")
        result = check_func()
        results.append(result)
    
    logger.info("\n" + "=" * 50)
    if all(results):
        logger.info("✓ All health checks passed!")
        return 0
    else:
        logger.error("✗ Some health checks failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
