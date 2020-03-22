import bson
import os
import pymongo
import time
from clients.twitterapi import TwitterAPI
from dateutil.parser import parse
from util.util import insert_in_mongo_by_hashtags


BEARER_TOKEN = os.environ['BEARER_TOKEN']
MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']
HASHTAGS = os.environ['HASHTAGS']

time.sleep(10) # Wait Mongo DB be ready

mongo_client = pymongo.MongoClient('mongodb://%s:%s@%s:27017/admin' % 
                                    (MONGO_ROOT_USERNAME, 
                                     MONGO_ROOT_PASSWORD, 
                                     MONGO_HOST))

tweets_collection = mongo_client.twitterDB.tweets
users_collection = mongo_client.twitterDB.users

twitter_api = TwitterAPI(BEARER_TOKEN)

hashtags_array = HASHTAGS.split(';')

while True:
    insert_in_mongo_by_hashtags(hashtags_array,
                                twitter_api,
                                tweets_collection, 
                                users_collection)

    time.sleep(600) # Hit again the Twitter API in the next 10 minutes