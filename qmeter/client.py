from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, List

from django.conf import settings



class MongoDBClient:
    HOST = settings.MONGO_HOST
    PORT = settings.MONGO_PORT
    DB_NAME = settings.MONGO_DB_NAME

    FEEDBACK_COLLECTION: str = "feedback_collection"
    # ...  can be added other collections

    def __init__(self, **kwargs):
        client = MongoClient(f"mongodb://{self.HOST}:{self.PORT}/{self.DB_NAME}")
        self.db = client[self.DB_NAME]
        self.feedback_collection: Collection = self.db[self.FEEDBACK_COLLECTION]
        

    def _get_data(self, collection: Collection, pipeline: List[Dict]) -> List[Dict]:
        return list(collection.aggregate(pipeline))

    def get_score_data(self) -> List[Dict]:
        
        # Pipeline-1
        pipeline: List[Dict] = [
            {
                "$unwind": "$feedback_rate"
            },

            {
                "$group": {
                    "_id": {
                        "branch_name": "$branch.name",
                        "service_name": "$feedback_rate.service.name",
                    },
                    
                    "ones": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 1] }, 1, 0] } },
                    "twos": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 2] }, 1, 0] } }, 
                    "threes": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 3] }, 1, 0] } },
                    "fours": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 4] }, 1, 0] } },
                    "fives": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 5] }, 1, 0] } },
                    
                }
            }, 
             
            {
                "$addFields":{
                    "total_count": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "branch_name": "$_id.branch_name",
                    "service_name": "$_id.service_name",
                    "ones": "$ones", 
                    "twos": "$twos", 
                    "threes": "$threes", 
                    "fours": "$fours", 
                    "fives": "$fives",
                    "total": "$total_count",
                    "score": { 
                        "$cond": { 
                            "if": { "$gt": [ { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] }, 0] },
                            "then": {
                                "$divide": [
                                    {
                                        "$multiply": [
                                            100,
                                            {
                                                "$add": [
                                                    { "$multiply": ["$ones", 10] },
                                                    { "$multiply": ["$twos", 5] },
                                                    { "$multiply": ["$fours", -5] },
                                                    { "$multiply": ["$fives", -10] }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "$multiply": [ "$total_count", 10]
                                    }
                                ]
                            },
                            "else": 0
                        }    
                    }
                }
            }
        ]

        return self._get_data(self.feedback_collection, pipeline)

    def get_score_data_by_branch(self) -> List[Dict]:
        # With this method there is no need to modify data for sending to the table

        # Pipeline-2
        pipeline: List[Dict] = [
            {
                "$unwind": "$feedback_rate"
            },
            {
                "$group": {
                    "_id": {
                        "branch_name": "$branch.name",
                        "service_name": "$feedback_rate.service.name"
                    },
                    "ones": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 1] }, 1, 0] }},
                    "twos": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 2] }, 1, 0] }},
                    "threes": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 3] }, 1, 0] }},
                    "fours": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 4] }, 1, 0] }},
                    "fives": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 5] }, 1, 0] }}
                }
            },
            {
                "$addFields": {
                    "total_count": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                    "weighted_sum": {
                        "$add": [
                            { "$multiply": ["$ones", 10] },
                            { "$multiply": ["$twos", 5] },
                            { "$multiply": ["$fours", -5] },    
                            { "$multiply": ["$fives", -10] }
                        ]
                    }
                }
            },
            {
                "$addFields": {
                    "score": {
                        "$cond": {
                            "if": { "$gt": ["$total_count", 0] },
                            "then": {
                                "$multiply": [
                                    { "$divide": [{ "$multiply": ["$weighted_sum", 100] }, { "$multiply": ["$total_count", 10] }] },
                                    1
                                ]
                            },
                            "else": 0
                        }
                    }  
                }
            },
            {
                "$group": {
                    "_id": "$_id.branch_name",
                    "services": {
                        "$push": {
                            "service_name": "$_id.service_name",
                            "score": "$score",
                            
                            "ones": "$ones",
                            "twos": "$twos",
                            "threes": "$threes",
                            "fours": "$fours",
                            "fives": "$fives",

                            "total": "$total_count",

                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "branch_name": "$_id",
                    "services": 1
                }
            },
        ]

        return self._get_data(self.feedback_collection, pipeline)



