# Use lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY tests/ /app/tests/

RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run tests
CMD ["pytest", "-v", "/app/tests/test_critical_suite.py"]