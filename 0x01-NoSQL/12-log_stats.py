#!/usr/bin/env python3
"""
12-log_stats.py
"""
import pymongo


def log_stats():
    """
    a Python script that provides some stats about,
    Nginx logs stored in MongoDB
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    methods_counts = {method: collection.count_documents({"method": method}) for method in methods}

    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {methods_counts[method]}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
