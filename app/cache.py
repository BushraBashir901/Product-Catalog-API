import redis
import json
from app.config import settings  # loads REDIS_URL from environment

# Connect to Redis
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Initialize cache (optional, just to test connection)
def init_cache():
    try:
        r.ping()
        print("Redis is connected and ready!")
    except redis.exceptions.ConnectionError as e:
        print("Redis connection failed:", e)

# Get data from cache
def get_cache(key: str):
    value = r.get(key)
    if value:
        return json.loads(value)  # convert JSON string back to Python object
    return None

# Set data to cache
def set_cache(key: str, value, expire: int = 60):
    r.set(key, json.dumps(value), ex=expire)

# Delete a key from cache (used when data changes)
def delete_cache(key: str):
    r.delete(key)