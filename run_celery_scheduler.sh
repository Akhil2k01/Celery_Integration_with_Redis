#!/bin/sh

echo "Running Celery Scheduler."
. redis-venv/bin/activate && python3 -m celery -A  redis_celery_integration.celery beat -l info -f celery_scheduler.log
