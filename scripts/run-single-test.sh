#!/bin/bash
TEST_NAME=$1
PRIORITY=${2:-critical}  # Default to critical priority

if [ -z "$TEST_NAME" ]; then
    echo "Usage: ./run-single-test.sh <test_name> [priority]"
    exit 1
fi

JOB_NAME="manual-test-$(date +%s)"

# Create job from the base job template
kubectl create job $JOB_NAME \
  --namespace mobile-testing \
  --from template/mobile-test \
  -- pytest -v -k "$TEST_NAME" /app/tests/test_${PRIORITY}_suite.py

echo "Waiting for job to start..."
sleep 5

POD_NAME=$(kubectl get pods -n mobile-testing -l job-name=$JOB_NAME -o jsonpath='{.items[0].metadata.name}')
kubectl logs -f -n mobile-testing $POD_NAME