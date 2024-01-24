#!/usr/bin/env python3
"""
exercise.py
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        key = method.__qualname__

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8") if d is not None else None)

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=lambda d: int(d) if d is not None else None)

if __name__ == "__main__":
    cache = Cache()

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))
