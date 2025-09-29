#!/bin/bash

# Navigate to the backend directory
cd /app

# Install Python dependencies, including openai, pydantic, and pydantic-core
pip install -r requirements.txt

# Run the Flask application
python src/main.py


