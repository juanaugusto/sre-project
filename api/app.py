from flask import Flask

app = Flask(__name__)

@app.route("/what/users/most/followers")
def what_users_with_most_followers():
    # Quais são os 5 (cinco) usuários, da 
    # amostra coletada, que possuem mais
    # seguidores?
    return "oi"

@app.route("/total/tweets/hour/<int:year>/<int:month>/<int:day>")
def total_tweets_per_hour(year, month, day):
    # Qual o total de postagens, agrupadas
    # por hora do dia (independentemente da
    # hashtag)?
    return "Hello, Wolddd!"

@app.route("/total/tweets/hashtag/language/location")
def total_tweets_per_hashtag_and_language_location():
    # Qual o total de postagens
    # para cada uma das #tag por idioma/país do
    # usuário que postou;
    return "oi"