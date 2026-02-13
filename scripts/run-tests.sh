#!/bin/bash

# Exit on error
set -e

echo "Running ArXiv Recommendation System tests..."

# Run backend tests
echo "Running backend tests..."
cd backend
python -m pytest tests/ -v

# Run frontend tests
echo "Running frontend tests..."
cd ../client
npm test -- --watchAll=false

echo "All tests completed successfully!" 