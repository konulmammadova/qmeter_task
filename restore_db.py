import requests
import pymongo
from pymongo import MongoClient

# MongoDB connection URI
MONGO_URI = 'mongodb://localhost:27017/qmeter_feedback_db'
client = MongoClient(MONGO_URI)
db = client['qmeter_feedback_db']
collection = db['feedback_collection']

# URL of the JSON data
json_url = 'https://qmeter-fb-dev.s3.amazonaws.com/media/feedback.json'

# Download the JSON data
response = requests.get(json_url)
response.raise_for_status()  # Check for errors

# Load JSON data
data = response.json()

# Insert data into MongoDB
# Assuming data is a list of documents
if isinstance(data, list):
    result = collection.insert_many(data)
else:
    result = collection.insert_one(data)

print(f"Inserted documents with IDs: {result.inserted_ids if isinstance(result, pymongo.results.InsertManyResult) else result.inserted_id}")





db.feedback_collection.aggregate(
    [
    {
        $group: {
            _id: {
                branch_name: "$branch.name", 
                service_name: "$feedback_rate.service.name"
            },
            ones: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 1] }, 1, 0]} },
            twos: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 2] }, 1, 0]} },
            threes: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 3] }, 1, 0]} },
            fours: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 4] }, 1, 0]} },
            fives: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 5] }, 1, 0]} }
        }    
    },
    {
        $project: {
            _id: 0,
            branch_name: "$_id.branch_name",
            service_name: "$_id.service_name",
            score: {
                $cond: {
                    if: { $gt: [{ $sum: ["$ones", "$twos", "$threes", "$fours", "$fives"] }, 0] },
                    then: {
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
                    else: 0
                }
            }
        }
    }
]
)
