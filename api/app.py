import bson
import logging
import os
import pymongo
from bson.son import SON
from flask import Flask
from flask import jsonify
from flask import request
from log.log import ContextFilter
from prometheus_flask_exporter import PrometheusMetrics
from pygelf import GelfUdpHandler


MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']

mongo_client = pymongo.MongoClient('mongodb://%s:%s@%s:27017/admin' % 
                                    (MONGO_ROOT_USERNAME, 
                                     MONGO_ROOT_PASSWORD, 
                                     MONGO_HOST))

tweets_collection = mongo_client.twitterDB.tweets
users_collection = mongo_client.twitterDB.users

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.addFilter(ContextFilter())
logger.addHandler(GelfUdpHandler(host='graylog', port=12201, include_extra_fields=True))

@app.route("/what/users/most/followers")
def what_users_with_most_followers():
    logging.info('Starting to get what user have most followers...')

    # Get users in descending order of the amount of followers
    users = users_collection.find() \
                .sort([('user_followers_count', pymongo.DESCENDING)]) \
                .limit(5)

    users = [{'user_id': user['user_id'], 
              'user_name': user['user_name'],
              'user_followers_count': user['user_followers_count']} 
              for user in users]

    logging.info('Finished to get what user have most followers...')
    return jsonify({'users': users})

@app.route("/total/tweets/hour")
def total_tweets_per_hour():
    logging.info('Starting to get total of tweets per hour of day...')  

    # Aggregate tweets by the hour that they were created, 
    # and for each hour count how many tweets were created in this hour
    hours = tweets_collection.aggregate([
        {"$group": {"_id": "$tweet_hour_created_at", "count": {"$sum": 1}}},
        {"$sort": SON([("_id", +1)])}        
    ])

    hours = [{'hour': hour['_id'], 'count': hour['count']} for hour in hours]

    logging.info('Finished to get total of tweets per hour of day...') 
    return jsonify({'hours': hours})

@app.route("/total/tweets/hashtag/language/location/<int:user_id>")
def total_tweets_per_hashtag_and_language_location(user_id):
    logging.info('Starting to get total of tweets per hashtag and language location of user %s' % user_id)
    
    # First get the user with that has that user_id
    user = users_collection.find_one({'user_id': user_id})
    logging.debug('User %s has produced %s tweets...' % (user_id, len(user['tweets'])))

    # Now, get all tweets of the user above,
    # group them by tweet_hashtag and tweet_lang
    # and count the amout of tweets that has the same
    # tweet_hashtag and tweet_lang 
    results = tweets_collection.aggregate([
        {'$match': {'_id': {"$in": user['tweets']}}},
        {'$group': {"_id": {'tweet_hashtag': "$tweet_hashtag", 
                            'tweet_lang': "$tweet_lang"},
                    "count": {"$sum": 1}}},
        {"$sort": SON([("_id", +1)])}
    ])
        
    counts = [{'tweet_info': {'tweet_hashtag': result['_id']['tweet_hashtag'], 
                              'tweet_lang': result['_id']['tweet_lang'],
               'count': result['count']}} 
               for result in results]

    logging.info('Finished to get total of tweets per hashtag and language location of user %s' % user_id)
    return jsonify({'infos': counts})

@app.errorhandler(404)
def page_not_found(e):
    logging.warning('Not found!')
    return jsonify({'message': 'Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.critical('Internal Server Error')
    return jsonify({'message': 'Internal Server Error'}), 500
