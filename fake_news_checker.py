from twython import Twython
from flask import Markup

from get_score import get_score_data
import helpers, json

# Get Twitter API credentials from a plain text file
APP_KEY, ACCESS_TOKEN = helpers.get_credentials()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

def check(news_string):
    tweets = get_relevant_tweets(news_string)
    score = get_score_data(tweets)
    related = [tweets[0]['id'], tweets[1]['id'], tweets[2]['id']]
    return {'truthfullness': score['credScore'],
            'probability': score['credScore']/100,
            'related_tweets': list(map(lambda x: Markup(twitter.get_oembed_tweet(id=x)['html']), related)),
            'strongPosTweets': score['strongPosTweets'],
            'nTweets': score['nTweets']}

def get_relevant_tweets(subject):
    res = []

    count = 0
    lastId = None
    canFindTweets = True
    subj = subject
    subject += ' -filter:retweets'
    while (count < 20) and canFindTweets:
        if lastId is None:
            searchResults = twitter.search(q=subject,
                                            count=100,
                                            lang='en')['statuses']
        else:
            searchResults = twitter.search(q=subject,
                                            count=100,
                                            lang='en',
                                            max_id=lastId)['statuses']

        searchResults = sorted(searchResults, key=lambda tweet: tweet['id'])
        if len(searchResults) < 100:
            canFindTweets = False
        else:
            lastId = searchResults[0]['id']

        print(lastId)
        res += searchResults
        count += 1
    print('{} tweets found for subject \"{}\"'.format(len(res), subj))

    return res
