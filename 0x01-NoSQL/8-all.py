#!/usr/bin/env python3
"""
8-all.py
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    a Python function that lists all documents in a collection
    """
    return list(mongo_collection.find())
