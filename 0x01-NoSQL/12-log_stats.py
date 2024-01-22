#!/usr/bin/env python3
"""
12-log_stats.py
"""
from pymongo import MongoClient


def log_stats():
    """
    a Python script that provides some stats about,
    Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check_count = logs_collection.count_documents(
        {"method": "GET", "path": "/status"}
        )
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    log_stats()
