import os
import pymongo
import time
from clients.twitterapi import TwitterAPI
from util.util import insert_in_mongo_by_statuses
from util.util import get_mongo_client


if __name__ == '__main__':
    API_KEY = os.environ['API_KEY']
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
    MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
    MONGO_HOST = os.environ['MONGO_HOST']
    HASHTAGS = os.environ['HASHTAGS']

    mongo_client = get_mongo_client(MONGO_ROOT_USERNAME,
                                    MONGO_ROOT_PASSWORD,
                                    MONGO_HOST)

    tweets_collection = mongo_client.twitterDB.tweets
    users_collection = mongo_client.twitterDB.users

    twitter_api = TwitterAPI(API_KEY, API_SECRET_KEY)

    hashtags_array = HASHTAGS.split(';')

    while True:
        insert_in_mongo_by_statuses(hashtags_array,
                                    twitter_api,
                                    tweets_collection, 
                                    users_collection)

        # Hit again the Twitter API only in the next 10 minutes
        time.sleep(600)