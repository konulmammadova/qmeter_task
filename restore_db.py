import requests
import pymongo
from pymongo import MongoClient
from django.conf import settings

# settings.configure()


client = MongoClient(f"mongodb://localhost:27017/qmeter_feedback_db'")
db = client["qmeter_feedback_db"]
collection = db['feedback_collection']

json_url = 'https://qmeter-fb-dev.s3.amazonaws.com/media/feedback.json'

response = requests.get(json_url)
response.raise_for_status()

data = response.json()

# Insert data into MongoDB
if isinstance(data, list):
    result = collection.insert_many(data)
else:
    result = collection.insert_one(data)

print(f"Inserted documents with IDs: {result.inserted_ids if isinstance(result, pymongo.results.InsertManyResult) else result.inserted_id}")
