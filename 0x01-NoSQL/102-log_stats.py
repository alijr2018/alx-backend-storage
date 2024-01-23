#!/usr/bin/env python3
"""
102-log_stats.py
"""
import pymongo


def log_stats():
    """
    Improve 12-log_stats.py by adding the top 10,
    of the most present IPs in the collection nginx,
    of the database logs.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    methods_counts = {method: collection.count_documents({"method": method.lower()}) for method in methods}

    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    top_ips = list(collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]))

    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {methods_counts[method]}")
    print(f"{status_check_count} status checks")
    print("IPs:")
    for ip_info in top_ips:
        print(f"\t{ip_info['_id']}: {ip_info['count']}")

if __name__ == "__main__":
    log_stats()
