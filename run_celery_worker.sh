#!/bin/sh

echo "Running Concurrent Worker."
. redis-venv/bin/activate && python3 -m celery -A  redis_celery_integration.celery worker -l info -f celery_worker.log