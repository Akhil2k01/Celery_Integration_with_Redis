import logging
from flask_restful import Resource, reqparse
from redis_celery_integration import add_monitor_task, add_destroy_task

class MiddleLayer(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            'redis_name',
            type=str,
            required=False,
            location='json',
            help=''
        )

    def post(self):
        try:
            args = self.req_parse.parse_args()
            redis_name = args.get("redis_name","")
            logging.info(f"Adding task for redis : {redis_name}")
            monitor_task = add_monitor_task(frequency=10, redis_name=redis_name)
            logging.info(f"Added Monitor Task {monitor_task}")
            destroy_task = add_destroy_task(frequency=15, redis_name=redis_name)
            logging.info(f"Added Destroy Task {destroy_task}")
            return {'message': 'Scheduled an execution for the redis: {}'.format(redis_name),'statusCode': 200}
        except Exception as err:
            logging.error(f"ERROR: {err}")
            return {'message': str(err),'statusCode': 400}, 400