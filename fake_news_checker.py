import twython
from flask import Markup

APP_KEY = 'eEpld5TDoB634G69O4cQFXCWy'
APP_SECRET = 'YQZK4ghbPmik9b357j80tRS1ux4c5l0uDCVFR0LLgVb0WKzlYG'

OAUTH_TOKEN = '919630313919303680-AulT475Gh7c7XeUJQUAzlciCQgDT4ok'
OAUTH_TOKEN_SECRET = 'P4oMPAGfcvBhVrjnDYlHMmwpHh4P4AETrjGxCrJroOlB3'

def check(search_string):
    truthfullness = 64

    twitter = twython.Twython(APP_KEY, APP_SECRET,
                              OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    if search_string=="trump-missile-launch":
        truthfullness = 4
    elif search_string=="walcott-leaves-arsenal":
        truthfullness = 20
    elif search_string=="sanchez-transfer":
        truthfullness = 98

    related_tweets = [980567693089701890, 979887418370330624, 979861054296530944]

    return {'truthfullness': truthfullness,
            'probability': truthfullness/100,
            'related_tweets': list(map(lambda x: Markup(twitter.get_oembed_tweet(id = x)['html']), related_tweets))}

