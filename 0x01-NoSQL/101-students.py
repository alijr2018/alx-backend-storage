#!/usr/bin/env python3
"""
101-students.py
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    a Python function that returns all students,
    sorted by average score.
    """
    main = [{
        "$project": {
            "name": 1,
            "topics": 1,
            "averageScore": {
                "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
                }
            }
        ]
    return list(mongo_collection.aggregate(main))
