import os
import requests

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.results import InsertManyResult

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fetches data from a URL as json and inserts into MongoDB'

    def handle(self, *args, **kwargs):
        MONGO_HOST = os.getenv("MONGO_HOST")
        MONGO_PORT = os.getenv("MONGO_PORT")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

        client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}")
        database = client[MONGO_DB_NAME]
        collection = database['feedback_collection']

        json_url = 'https://qmeter-fb-dev.s3.amazonaws.com/media/feedback.json'


        response = requests.get(json_url)
        response.raise_for_status()
        data = response.json()

        # Insert data 
        try:
            if isinstance(data, list):
                result = collection.insert_many(data)
            else:
                result = collection.insert_one(data)
            self.stdout.write(f"Inserted documents with ids: {result.inserted_ids if isinstance(result, InsertManyResult) else result.inserted_id}")
        except PyMongoError as e:
            self.stderr.write(f"Error raised while inserting documents: {e}")