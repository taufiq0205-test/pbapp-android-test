# Base stage for common dependencies
FROM python:3.9-slim AS base
WORKDIR /app
RUN apt-get update && \
    apt-get install -y android-sdk-platform-tools && \
    apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests/conftest.py tests/pytest.ini /app/tests/
ENV PYTHONPATH=/app

# Critical priority stage
FROM base AS critical
LABEL test_priority=critical
COPY tests/test_critical_suite.py /app/tests/
COPY tests/Critical /app/tests/Critical
CMD ["pytest", "-v", "-m", "critical", "tests/test_critical_suite.py"]

# High priority stage
FROM base AS high
LABEL test_priority=high
COPY tests/test_high_suite.py /app/tests/
COPY tests/High /app/tests/High
CMD ["pytest", "-v", "-m", "high", "tests/test_high_suite.py"]

# Medium priority stage
FROM base AS medium
LABEL test_priority=medium
COPY tests/test_medium_suite.py /app/tests/
COPY tests/Medium /app/tests/Medium
CMD ["pytest", "-v", "-m", "medium", "tests/test_medium_suite.py"]