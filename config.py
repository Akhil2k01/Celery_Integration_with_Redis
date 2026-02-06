import json

def read_json_config():
    config_file_path = 'config.json'
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    config_file.close()
    return config

def fetch_config_values():  # called in the config.py file
    """
    Fetching the app configuration values from either param store or config.json
    returns: a dict with all required keys and values
    """

    print("Fetching the config values for the app")
    config = read_json_config()
    print(f"Fetched the config values: {config}")
    return config  # returning dict

class Config(object):
    """
    This class is used to fetch the configuration values for the app
    """

    config = fetch_config_values()

    REDBEAT_BROKER_URL = config.get("REDBEAT_SCHEDULER", dict()).get('BROKER_URL', 'redis://localhost:6379/5')
    REDBEAT_RESULT_BACKEND = config.get("REDBEAT_SCHEDULER", dict()).get('RESULT_BACKEND', 'redis://localhost:6379/6')
    REDBEAT_REDIS_URL = config.get("REDBEAT_SCHEDULER", dict()).get('REDBEAT_REDIS_URL', 'redis://localhost:6379/7')