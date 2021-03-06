import bson
import os
import pymongo
import time
from clients.twitterapi import TwitterAPI
from dateutil.parser import parse


def get_mongo_client(MONGO_ROOT_USERNAME, 
                     MONGO_ROOT_PASSWORD, 
                     MONGO_HOST):
    """Gets mongo client up until it is available."""
    # Retrying up until Mongo is available
    while True:
        try:
            mongo_client = pymongo.MongoClient(
                           'mongodb://%s:%s@%s:27017/admin' % 
                           (MONGO_ROOT_USERNAME, 
                            MONGO_ROOT_PASSWORD, 
                            MONGO_HOST),
                            serverSelectionTimeoutMS=4000)
            mongo_client.server_info()
            return mongo_client
        except:
            print('Retrying Mongo connection...')


def update_user_in_mongo(user, users_collection):
    """Updates only one user in Mongo."""
    users_collection.find_one_and_update(
        {"_id": user['_id']}, 
        {"$set": user}, 
        upsert=True
    )


def insert_tweet_in_mongo(tweet, 
                          tweets_collection):
    """Inserts one tweet in Mongo."""
    if tweets_collection.find_one({'tweet_id': tweet['tweet_id']}) is None:
        tweets_collection.insert_one(tweet)


def insert_user_in_mongo(user,
                         users_collection):
    """Inserts one user in Mongo."""
    if users_collection.find_one({'user_id': user['user_id']}) is None:
        users_collection.insert_one(user)


def insert_tweets_in_mongo(tweets, 
                           tweets_collection):
    """Inserts tweets in Mongo."""
    for tweet in tweets:
        insert_tweet_in_mongo(tweet, tweets_collection)


def insert_users_in_mongo(users, 
                          users_collection):
    """Inserts users in Mongo."""
    for user in users:
        insert_user_in_mongo(user, users_collection)


def find_tweets_by_tweets_ids(tweets_ids,
                              tweets_collection):
    """Find tweets in Mongo by array of tweets ids."""
    results = tweets_collection.find(
        {'tweet_id': {"$in": tweets_ids}},
    )

    return [result['_id'] for result in results]


def insert_references_from_users_to_tweets_in_mongo(references,
                                                    tweets_collection,
                                                    users_collection):
    """Given references from users to tweets, insert them in Mongo."""    
    for user_id, tweets_ids in references.items():

        user = users_collection.find_one({'user_id': user_id})
        user['tweets'] += find_tweets_by_tweets_ids(tweets_ids, 
                                                    tweets_collection)
        user['tweets'] = list(set(user['tweets']))
        update_user_in_mongo(user, users_collection)


def get_users_with_tweets_references(statuses):
    """Given statuses, for each unique user id, points them to all its tweets."""
    references = [{'user_id': status['user']['id'], 
                   'tweets_ids': []} 
                   for status in statuses]

    references = {}
    for status in statuses:
        if status['user']['id'] not in references:
            references[status['user']['id']] = []

    for status in statuses:
        references[status['user']['id']] += [status['id']]   

    return references     


def insert_in_mongo_by_hashtag(statuses, 
                               hashtag,
                               tweets_collection,
                               users_collection):
    """Inserts in Mongo tweets and users given a specific hashtag."""
    users = [{'user_id': status['user']['id'],
              'user_name': status['user']['name'],
              'user_followers_count': status['user']['followers_count'],
              'user_location': status['user']['location'],
              'tweets': []}
             for status in statuses]

    tweets = [{'tweet_hashtag': hashtag,
               'tweet_id': status['id'],
               'tweet_text': status['text'],
               'tweet_hour_created_at': parse(status['created_at']).hour,
               'tweet_lang': status['lang']}
             for status in statuses]

    insert_users_in_mongo(users, 
                          users_collection)
    insert_tweets_in_mongo(tweets, 
                           tweets_collection)
    insert_references_from_users_to_tweets_in_mongo(
        get_users_with_tweets_references(statuses),
        tweets_collection,
        users_collection
    )


def insert_in_mongo_by_statuses(hashtags,
                                twitter_api,
                                tweets_collection,
                                users_collection):
    """Inserts in Mongo tweets and users for each hashtag."""
    for hashtag in hashtags:

        statuses = twitter_api.search_statuses(hashtag, 100)
        insert_in_mongo_by_hashtag(statuses, 
                                   hashtag, 
                                   tweets_collection, 
                                   users_collection)
