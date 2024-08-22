from pymongo import MongoClient
from django.conf import settings



class MongoDBClient:
    HOST = settings.MONGO_HOST
    PORT = settings.MONGO_PORT
    DB_NAME =settings.MONGO_DB_NAME

    FEEDBACK_COLLECTION = "feedback_collection"

    def __init__(self, **kwargs):
        client = MongoClient(f"mongodb://{self.HOST}:{self.PORT}/{self.DB_NAME}")
        self.db = client[self.DB_NAME]
        self.feedback_collection = self.db[self.FEEDBACK_COLLECTION]
        # ...  can be written other collections

    def _get_data(self, collection, pipeline):
        return list(collection.aggregate(pipeline))

    def get_score_data(self):
        pipeline = [
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
                "$project": {
                    "_id": 0,
                    "branch_name": "$_id.branch_name",
                    "service_name": "$_id.service_name",
                    "ones": "$ones", 
                    "twos": "$twos", 
                    "threes": "$threes", 
                    "fours": "$fours", 
                    "fives": "$fives",
                    "total": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                    "score": { 
                        "$cond": { 
                            "if": { "$gt": [ { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] }, 0] },
                            "then": {
                                "$divide": [
                                    {
                                        "$multiply": [
                                            100,
                                            {
                                                "$sum": [
                                                    { "$multiply": ["$ones", 10] },
                                                    { "$multiply": ["$twos", 5] },
                                                    { "$multiply": ["$fours", -5] },
                                                    { "$multiply": ["$fives", -10] }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "$multiply": [
                                            { "$sum": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                                            10
                                        ]
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

    def get_score_data_by_branch(self):
        """
            With this method there is no need to modify data for sending to the table
        """
        pipeline=[
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
                    "total": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                    "weightedSum": {
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
                        "$round": [
                            {
                                "$cond": {
                                    "if": { "$gt": ["$total", 0] },
                                    "then": {
                                        "$multiply": [
                                            { "$divide": [{ "$multiply": ["$weightedSum", 100] }, { "$multiply": ["$total", 10] }] },
                                            1
                                        ]
                                    },
                                    "else": 0
                                }
                            },
                            0
                        ]
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

                            "total": "$total",

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
            }
        ]

        return self._get_data(self.feedback_collection, pipeline)



