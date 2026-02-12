# Celery_Integration_with_Redis


## This is a simple project of implementing celery async processing with Redis backend and message broker

Celery is a distributed task queue. It allows you to run time-consuming operations in the background as asynchronous tasks. Celery handles task scheduling, distribution, and execution, making it an essential tool for creating responsive applications.

Redis is an in-memory data structure store, widely used as a message broker for Celery. It manages the task queues efficiently, making it a perfect choice for real-time messaging systems.

This repo has a code in which celery and redis have been integrated to work together.

Required Packages:
1. Redis
2. Celery
3. USe requirements.txt file to install python packages

Note: Run all these processes in different terminals or run it as a background, for debugging you can use the log file created for each processes.
You are set to run the app.py 
```
python3 app.py or bash run_app.sh
```
Once app.py is running run the remaining 2 .sh files
```
bash run_celery_scheduler.sh
bash run_celery_worker.sh
```
Running these 2 files with start the celery scheduler and worker, which actually are responsible in running the async tasks

Once all processes are running, call the api using curl command
```
curl -H "Content-Type: application/json" -X POST "http://localhost:3000/start_redis_task" -d '{"redis_name":"my_redis"}'
```
This will creates 2 simple periodic tasks, monitor and destroy. We can add more tasks based on our needs.

Note: You can also adjust the celery backend and broker URL in config.json file.
