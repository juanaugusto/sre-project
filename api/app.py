import bson
import os
import pymongo
from bson.son import SON
from flask import Flask
from flask import jsonify
from prometheus_client import make_wsgi_app
from flask import request
from prometheus_flask_exporter import PrometheusMetrics


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


@app.route("/what/users/most/followers")
def what_users_with_most_followers():
    # Quais são os 5 (cinco) usuários, da 
    # amostra coletada, que possuem mais
    # seguidores?

    users = users_collection.find() \
                .sort([('user_followers_count', pymongo.DESCENDING)]) \
                .limit(5)

    users = [{'user_id': user['user_id'], 
              'user_name': user['user_name'],
              'user_followers_count': user['user_followers_count']} 
              for user in users]

    return jsonify({'users': users})

@app.route("/total/tweets/hour")
def total_tweets_per_hour():
    # Sat Mar 21 16:00:50 +0000 2020
    # Qual o total de postagens, agrupadas
    # por hora do dia (independentemente da
    # hashtag)?
    
    hours = tweets_collection.aggregate([
        {"$group": {"_id": "$tweet_hour_created_at", "count": {"$sum": 1}}},
        {"$sort": SON([("_id", +1)])}        
    ])

    hours = [{'hour': hour['_id'], 'count': hour['count']} for hour in hours]

    return jsonify({'hours': hours})

@app.route("/total/tweets/hashtag/language/location/<int:user_id>")
def total_tweets_per_hashtag_and_language_location(user_id):
    # Qual o total de postagens
    # para cada uma das #tag por idioma/país do
    # usuário que postou;

    user = users_collection.find_one({'user_id': user_id})

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

    return jsonify({'infos': counts})
