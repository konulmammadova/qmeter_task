from pymongo import MongoClient

# MongoDB connection settings
MONGO_URI = 'mongodb://mongodb:27017/qmeter_feedback_db' #'mongodb://container_name:27017/database_name'
# you can use like following #
#############################
# load config from .env file
# from dotenv import load_dotenv
# load_dotenv()
# MONGO_URI = os.environ["MONGO_URI"]
#############################


# MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
# MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
# MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'your_database_name')

# client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
# db = client[MONGO_DB_NAME]
#############################

# Create a MongoClient instance
client = MongoClient(MONGO_URI)
db = client['qmeter_feedback_db']

collection = db['feedback_collection']

def get_score_data():
    collection = db['feedback_collection']
   
    pipeline0 = [
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
                "total": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] }, # addField for readabily, time dont matter
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

    pipeline = [
        {
            "$unwind": "$feedback_rate"
        },

        # Group stage
        {
            "$group": {
                "_id": {
                    "branch_name": "$branch.name",
                    "service_name": "$feedback_rate.service.name"
                },
                # "ones": {"$sum": {"$cond": [{"$eq": ["$feedback_rate.rate_option", 1]}, 1, 0]}},
                # "twos": {"$sum": {"$cond": [{"$eq": ["$feedback_rate.rate_option", 2]}, 1, 0]}},
                # "threes": {"$sum": {"$cond": [{"$eq": ["$feedback_rate.rate_option", 3]}, 1, 0]}},
                # "fours": {"$sum": {"$cond": [{"$eq": ["$feedback_rate.rate_option", 4]}, 1, 0]}},
                # "fives": {"$sum": {"$cond": [{"$eq": ["$feedback_rate.rate_option", 5]}, 1, 0]}}
            }
        },
        # Project stage
        {
            "$project": {
                "_id": 0,
                "branch_name": "$_id.branch_name",
                "service_name": "$_id.service_name",


                # added 
                # "ones": "$ones", 
                # "twos": "$twos", 
                # "threes": "$threes", 
                # "fours": "$fours", 
                # "fives": "$fives",
                # "sum_of_rate_options": {"$sum":["$ones", "$twos", "$threes", "$fours", "$fives"]},
                #

                "score": {
                    "$cond": {
                        "if": {"$gt": [
                            {"$sum": ["$ones", "$twos", "$threes", "$fours", "$fives"]}, 0]},
                        "then": {
                            "$multiply": [
                                {
                                    "$divide": [
                                        {
                                            "$multiply": [
                                                100,
                                                {
                                                    "$sum": [
                                                        {"$multiply": ["$ones", 10]},
                                                        {"$multiply": ["$twos", 5]},
                                                        {"$multiply": ["$fours", -5]},
                                                        {"$multiply": ["$fives", -10]}
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "$multiply": [
                                                {"$sum": ["$ones", "$twos", "$threes", "$fours", "$fives"]},
                                                10
                                            ]
                                        }
                                    ]
                                },
                                1
                            ]
                        },
                        "else": 0
                    }
                }
            }
        },
       
    ]

    result = { "data": list(collection.aggregate(pipeline0)) }

    return result


def get_service_scores_by_branch():
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
    
    result = { "data": list(collection.aggregate(pipeline)) }
   
    return result
