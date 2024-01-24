#!/usr/bin/env python3
"""
exercise.py
"""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def invokers(self, *args, **kwargs) -> Any:
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invokers


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def invokers(self, *args, **kwargs) -> Any:
        i_k = '{}:inputs'.format(method.__qualname__)
        o_k = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(i_k, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(o_k, output)
        return output
    return invokers


def replay(y: Callable) -> None:
    if y is None or not hasattr(y, '__self__'):
        return
    redis_stores = getattr(y.__self__, '_redis', None)
    if not isinstance(redis_stores, redis.Redis):
        return
    fix = y.__qualname__
    i_k = '{}:inputs'.format(fix)
    o_k = '{}:outputs'.format(fix)
    count = 0
    if redis_stores.exists(fix) != 0:
        count = int(redis_stores.get(fix))
    print('{} was called {} times:'.format(fix, count))
    fix_in = redis_stores.lrange(i_k, 0, -1)
    fix_out = redis_stores.lrange(o_k, 0, -1)
    for fxn_input, fxn_output in zip(fix_in, fix_out):
        print('{}(*{}) -> {}'.format(
            fix,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self, key: str, y: Callable = None,
            ) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        return y(data) if y is not None else data

    def get_str(self, key: str) -> str:
        return self.get(key, lambda z: z.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, lambda z: int(z))
