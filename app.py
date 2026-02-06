from flask import Flask, render_template
import redis
import time
import json
from middle_layer import MiddleLayer

from flask_restful import Api

import logging

app = Flask(__name__)
api = Api(app=app)

"""
curl -H "Content-Type: application/json" -X POST "http://localhost:3000/start_redis_task" -d '{"redis_name":"akhil_redis"}'
"""
api.add_resource(MiddleLayer, '/start_redis_task')

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', format='%(asctime)s - %(name)s - \
        %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("hello world...")
    app.run(host="0.0.0.0", port=3000, debug=True)
    