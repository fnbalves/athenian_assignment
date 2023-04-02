import redis
import json
import os

def read_env(key: str, default_value='') -> str:
    if key in os.environ:
        return os.environ[key]
    return default_value

REDIS_ADDRESS = read_env('REDIS_ADDRESS', 'localhost')
REDIS_PORT = read_env('REDIS_PORT', '6379')

redis_configuration = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)

def set_key(key, value):
    global redis_configuration
    redis_configuration.set(key, json.dumps(value))

def get_key(key):
    global redis_configuration
    return redis_configuration.get(key).decode('ascii')