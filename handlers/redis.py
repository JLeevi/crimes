from redis import Redis


def get_cached_file(file_name: str):
    redis_client = _get_redis_connection()
    cached_file = redis_client.get(file_name)
    if cached_file:
        return cached_file
    return None


def set_cached_file(file_name: str, file_content: bytes):
    redis_client = _get_redis_connection()
    redis_client.set(file_name, file_content)


def _get_redis_connection():
    redis_client = Redis(host='redis', port=6379,
                         db=0, decode_responses=False)
    return redis_client
