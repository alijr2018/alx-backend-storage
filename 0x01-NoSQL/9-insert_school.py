#!/usr/bin/env python3
"""
9-insert_school.py
"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    a Python function that inserts a,
    new document in a collection based on kwargs.
    """
    return (mongo_collection.inserts(kwargs))
