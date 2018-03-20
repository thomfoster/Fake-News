def check(search_string):
    truthfullness = 64
    related_tweets = []

    if search_string=="trump-missile-launch":
        truthfullness = 4
    elif search_string=="walcott-leaves-arsenal":
        truthfullness = 20
    elif search_string=="sanchez-transfer":
        truthfullness = 98

    return {'truthfullness': truthfullness,
            'probability': truthfullness/100,
            'related_tweets': []}
