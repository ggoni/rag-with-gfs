# RAG with Google Generative File Search (GFS)

Exploring and benchmarking Google's Generative File Search capabilities as a managed RAG solution.

## Project Overview

This project compares Google GFS (managed RAG) against custom RAG implementations to understand:
- Performance characteristics (latency, relevance, cost)
- Retrieval quality vs custom pipelines
- Use case suitability

## Setup

**Requirements**: Python 3.12, uv

```bash
# Install dependencies
uv sync

# Set API key
echo "GOOGLE_API_KEY=your_key_here" > .env
```

## Project Structure

- `data/`: Document corpus (gitignored)
- `notebooks/`: Jupyter exploratory notebooks
- `src/`: Reusable modules
- `models/`: GFS stores and custom RAG artifacts
- `reports/`: Analysis outputs

## Development

```bash
# Run EDA notebook
jupyter notebook notebooks/01_data_exploration.ipynb

# Run tests
pytest

# Format code
ruff format .
```
