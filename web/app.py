import logging
import os
import requests
from flask import Flask
from flask import jsonify
from flask import render_template


HOST_API = os.environ['HOST_API']

app = Flask(__name__)


def get_what_users_with_most_followers():
    response = requests.get('http://api:5000/what/users/most/followers', 
                           timeout=2)
    response.raise_for_status()
    return response.json()['users']


def get_total_tweets_per_hour():
    response = requests.get('http://api:5000/total/tweets/hour', 
                           timeout=2)
    response.raise_for_status()
    return response.json()['hours']


def get_total_tweets_per_hashtag_and_language_location(user_id):
    response = requests.get('http://api:5000/total/tweets/hashtag/language/location/%s' % user_id, 
                           timeout=2)
    response.raise_for_status()
    return response.json()['infos']

@app.route("/total/tweets/hashtag/language/location/<int:user_id>")
def html_total_tweets_per_hashtag_and_language_location(user_id):

    return \
        render_template('total_tweets_hashtag_language_location.html', 
                        total_tweets_per_hashtag_and_language_location=get_total_tweets_per_hashtag_and_language_location(user_id))

@app.route("/")
def home():

    return \
        render_template('index.html', 
                        what_users_with_most_followers=get_what_users_with_most_followers(),
                        total_tweets_per_hour=get_total_tweets_per_hour())
