
from redis import Redis


class BaseRepo:
    def __init__(self, redis: Redis):
        self.redis = redis
