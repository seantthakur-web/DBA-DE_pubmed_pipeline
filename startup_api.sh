#!/bin/bash
echo "Starting PubMed FastAPI server..."
uvicorn pubmed_pipeline.api.main:app --host 0.0.0.0 --port 8000

