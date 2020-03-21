import bson
import os
import pymongo
from flask import Flask
from flask import jsonify


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

@app.route("/what/users/most/followers")
def what_users_with_most_followers():
    # Quais são os 5 (cinco) usuários, da 
    # amostra coletada, que possuem mais
    # seguidores?
    # db.getCollection('users').find().sort( { user_followers_count: -1 } ).limit(5)

    users = users_collection.find() \
                .sort([('user_followers_count', pymongo.DESCENDING)]) \
                .limit(5)

    users = [{'user_id': user['user_id'], 
              'user_name': user['user_name'],
              'user_followers_count': user['user_followers_count']} 
              for user in users]

    return jsonify({'users': users})

@app.route("/total/tweets/hour/<int:year>/<int:month>/<int:day>")
def total_tweets_per_hour(year, month, day):
    # Qual o total de postagens, agrupadas
    # por hora do dia (independentemente da
    # hashtag)?
    return "Hello, Wolddd!"

@app.route("/total/tweets/hashtag/language/location/<user_name>")
def total_tweets_per_hashtag_and_language_location(user_name):
    # Qual o total de postagens
    # para cada uma das #tag por idioma/país do
    # usuário que postou;
    return "oi"