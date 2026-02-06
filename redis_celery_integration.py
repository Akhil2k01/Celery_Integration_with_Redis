import secrets
import celery
import redis
import random
import json
import os
from redbeat import RedBeatSchedulerEntry as Entry
from config import Config
import logging
from datetime import datetime, timezone

app = celery.Celery(__name__)

app.conf.update({
    'broker_url': Config.REDBEAT_BROKER_URL,
    'result_backend': Config.REDBEAT_RESULT_BACKEND,
    'redbeat_redis_url': Config.REDBEAT_REDIS_URL,
    'beat_scheduler': 'redbeat.RedBeatScheduler',
    'beat_max_loop_interval': 5,
    'beat_schedule': {}
})

def add_monitor_task(frequency=10, redis_name='test'):
    """
    Schedules a monitoring task.
    """
    task_name = secrets.token_urlsafe(6)
    task_entry = Entry(
        task_name,
        "redis_celery_integration.monitor_task",
        frequency,
        kwargs={'redis_name': redis_name},
        app=app
    )
    task_entry.save()
    task_entry.kwargs['entry_key'] = task_entry.key
    task_entry.save()
    logging.info("A monitor task has been added with the name: %s for redis_name: %s", task_name, redis_name)
    add_keys_to_json(task='monitor_task', redis_key=task_entry.key)
    return task_entry.key

def add_destroy_task(frequency=15, redis_name='test'):
    """
    Schedules a destroy task.
    """
    task_name = secrets.token_urlsafe(6)
    task_entry = Entry(
        task_name,
        "redis_celery_integration.destroy_task",
        frequency,
        kwargs={'redis_name': redis_name},
        app=app
    )
    task_entry.save()
    task_entry.kwargs['entry_key'] = task_entry.key
    task_entry.save()
    logging.info("A Destroy task has been added with the name: %s for redis_name: %s", task_name, redis_name)
    add_keys_to_json(task='destroy_task', redis_key=task_entry.key)
    return task_entry.key

def deregister_task(entry_key=''):
    """
    deregister a scheduled task.
    """
    if not entry_key:
        logging.info("Entry key value is invalid: %s", entry_key)
        return False
    try:
        e = Entry.from_key(key=entry_key, app=app)
        e.delete()
        logging.info("Redbeat Scheduler entry %s has been deleted", entry_key)
        return True
    except Exception as exc:
        logging.warning("Failed to delete RedBeat entry %s: %s", entry_key, exc)
        return False

@app.task(bind=True)
def monitor_task(self, redis_name, entry_key):
    logging.info("\n")
    rand_num = random.randint(1, 5)
    logging.info(f"Monitor task id is {self.request.id} for redis: {redis_name} and entry_key: {entry_key}")
    logging.info("Monitoring task for redis: {} with random number: {}".format(redis_name, rand_num))

    final_num = rand_num % 2
    logging.info("Final number for redis {} is {}".format(redis_name, final_num))
    if final_num == 0:
        logging.info("Final number is 0, deregistering the task for redis: {}".format(redis_name))
        deregister_task(entry_key=entry_key)
    return "Monitoring task executed for redis: {}".format(redis_name, rand_num)

@app.task(bind=True)
def destroy_task(self, redis_name, entry_key):
    logging.info("\n")
    logging.info(f"Destroy task id is {self.request.id} for redis: {redis_name} and entry_key: {entry_key}")

    # To validate before deleting the destroy task, added this check of monitor task exists or not in the redis
    if os.path.exists('redis_data.json'):
        with open('redis_data.json', 'r') as f:
            data = json.load(f)
        # Connect to the same Redis RedBeat uses
        redis_url = app.conf.get('redbeat_redis_url')
        r = redis.StrictRedis.from_url(redis_url)
        if not r.exists(data.get('monitor_task')):
            logging.info("Monitor task with entry key {} does not exist in Redis, deregistering the destroy task".format(data.get('monitor_task')))
            deregister_task(entry_key=entry_key)
            return "Destroy task is deregistered for redis: {}".format(redis_name)
        else:
            logging.info("Monitor task with entry key {} exists in Redis, not deregistering the destroy task".format(data.get('monitor_task')))
    else:
        logging.info("No json file found, deregistering the destroy task with entry key: {}".format(entry_key))
        deregister_task(entry_key=entry_key)
    return "Destroy task executed for redis: {}".format(redis_name)

# If needed to save the key info to a json file
def add_keys_to_json(task, redis_key):
    """
    This function is used to add the redis key and value to the json file
    """
    if os.path.exists('redis_data.json'):
        with open('redis_data.json', 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data[task] = redis_key
    # data[task+'_last_updated'] = str(datetime.now(tz=timezone.utc).replace(tzinfo=None, microsecond=0))
    data[task+'_last_updated'] = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Read the existing data from the json file: {data}")

    with open('redis_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"Added the {task} with redis key: {redis_key} to the json file")