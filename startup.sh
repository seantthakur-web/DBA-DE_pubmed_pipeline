#!/bin/bash

echo "Starting Streamlit App..."

PORT=8000

streamlit run ui/main.py --server.port $PORT --server.address 0.0.0.0
