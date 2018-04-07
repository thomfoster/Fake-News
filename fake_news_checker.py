import twython
from flask import Markup

def check(search_string, twitter):
    truthfullness = 64
    related_tweets = [982231162704637952, 982239010226487296, 982241282108960768]
    if search_string=="trump-missile-launch":
        truthfullness = 4
        related_tweets = [980567693089701890, 979887418370330624, 979861054296530944]
    elif search_string=="walcott-leaves-arsenal":
        truthfullness = 20
        related_tweets = [903247473375932416, 369483614796259328, 311925288558800896]
    elif search_string=="sanchez-transfer":
        truthfullness = 98
        related_tweets = [982229703187574786, 982222357212221441, 982199233762639874]


    return {'truthfullness': truthfullness,
            'probability': truthfullness/100,
            'related_tweets': list(map(lambda x: Markup(twitter.get_oembed_tweet(id = x)['html']), related_tweets))}

