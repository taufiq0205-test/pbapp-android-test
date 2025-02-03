# Base stage for common dependencies
FROM python:3.9-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests/conftest.py tests/pytest.ini /app/tests/
ENV PYTHONPATH=/app

# Critical priority stage
FROM base AS critical
COPY tests/test_critical_suite.py /app/tests/
COPY tests/Critical /app/tests/Critical
LABEL test_priority=critical \
      maintainer="autobots@photobook" \
      test_suite="critical-tests"
CMD ["pytest", "-v", "-m", "critical", "/app/tests/test_critical_suite.py"]

# High priority stage
FROM base AS high
COPY tests/test_high_suite.py /app/tests/
COPY tests/High /app/tests/High
CMD ["pytest", "-v", "-m", "high", "tests/test_high_suite.py"]

# Medium priority stage
FROM base AS medium
COPY tests/test_medium_suite.py /app/tests/
COPY tests/Medium /app/tests/Medium
CMD ["pytest", "-v", "-m", "medium", "tests/test_medium_suite.py"]