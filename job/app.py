import bson
import os
import pymongo
import time
from clients.twitterapi import TwitterAPI
from dateutil.parser import parse
from util.util import insert_in_mongo_by_statuses

if __name__ == '__main__':
    API_KEY = os.environ['API_KEY']
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
    MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
    MONGO_HOST = os.environ['MONGO_HOST']
    HASHTAGS = os.environ['HASHTAGS']

    time.sleep(60) # Wait Mongo DB be ready

    mongo_client = pymongo.MongoClient('mongodb://%s:%s@%s:27017/admin' % 
                                        (MONGO_ROOT_USERNAME, 
                                        MONGO_ROOT_PASSWORD, 
                                        MONGO_HOST))

    tweets_collection = mongo_client.twitterDB.tweets
    users_collection = mongo_client.twitterDB.users

    twitter_api = TwitterAPI(API_KEY, API_SECRET_KEY)

    hashtags_array = HASHTAGS.split(';')

    while True:
        insert_in_mongo_by_statuses(hashtags_array,
                                    twitter_api,
                                    tweets_collection, 
                                    users_collection)

        time.sleep(600) # Hit again the Twitter API in the next 10 minutes