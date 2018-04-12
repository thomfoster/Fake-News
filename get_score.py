#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, json, sys
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timezone
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#import dataset
data = pd.read_csv('twitter_topic_cred.csv')
x_data = data.loc[:,['in_reply_to_status_id_str',
       'created_at_ave_after_first_time', 'created_at_var', 
       'time_zone', 'time_zone_var', 
       'has_extended_profile', 'default_profile',
       'name_length_ave', 'created_at_ave_after_first_user',
       'followers_count_ave', 'followers_count_var',
       'favourites_count_ave',
       'screen_name_length_ave', 'screen_name_length_var', 'verified_no',
       'friends_count_ave','friends_count_var', 
       'statuses_count_ave', 'statuses_count_var', 'user_lang_non_English',
       'urls_no',
       'ave_hashtags',
       'favorite_count_ave','favorite_count_var',
       'place_non_null', 'text_length_ave',
       'retweet_count_ave','retweet_count_var','compound', 'compound_var'
       ]].values
                         
y_data = data.loc[:,'score'].values
 
from sklearn import preprocessing
#standardizing
scaler = preprocessing.StandardScaler().fit(x_data)
x_data_scaled = scaler.transform(x_data) 
#normalizing
normalizer = preprocessing.Normalizer().fit(x_data_scaled)
x_data_scaled_normal = normalizer.transform(x_data_scaled)
    
#linear kernel support vector machine
from sklearn import svm
lclf = svm.SVR(kernel = 'linear')
lclf.fit(x_data_scaled_normal, y_data)
    
    

#function that return credibility score
#tweets: a list of tweets json object
def get_score_data(tweets):
    n = len(tweets)
    
    tweetlist = []
    metrics = []
    outData = {}
    outData['nTweets'] = n
    
    #if tweets is a list of json object
    #for t in tweets:
    #   j = json.loads(t)
    #   tweetlist.append(j)
        
    #if tweets is a list of python dictionary already:
    tweetlist = tweets
      
    #1. in_reply_to_status_id_str
    x = 0
    res = 0.0
    for i in range(len(tweetlist)):
        if tweetlist[i]['in_reply_to_status_id_str'] != None:
            x=x+1
    res=x/n
    metrics.append(res)
    
    #2. created_at average after first time
    # timeseries is a list of creation time of tweets
    timeseries = []
    for x in range(len(tweetlist)):
        timeseries.append(datetime.strptime(tweetlist[x]['created_at'], '%a %b %d %H:%M:%S %z %Y'))
    earliesttime = timeseries[0]
    earliesttimeentry = 0
    latesttime = timeseries[0]
    latesttimeentry = 0
    for x in range(len(timeseries)):
        if timeseries[x] < earliesttime:
            earliesttime = timeseries[x]
            earliesttimeentry = x
        elif timeseries[x] > latesttime:
            latesttime = timeseries[x]
            latesttimeentry = x

    #earliesttime is the tweet in this topic which was written first and earliesttimeentry is which entry this is found at
    timesum = 0
    timesumsquare = 0
    for x in range(len(timeseries)):
        difference = timeseries[x] - earliesttime
        differencenumber = (difference.days)*24*60*60 + difference.seconds
        timesum = timesum + differencenumber
        timesumsquare = timesumsquare + differencenumber*differencenumber
    timeaverage = timesum/len(timeseries) 
    metrics.append(timeaverage)   
    
    #earliest tweets under the topic
    outData['earliestTweet'] = tweetlist[earliesttimeentry]
    outData['latestTweet'] = tweetlist[latesttimeentry]
    for i in range(len(timeseries)):
        timeseries[i] = timeseries[i].isoformat()
    outData['creationTimes'] = timeseries
    
    #3. created_at Variance 
    timevariance = ((timesumsquare)/len(timeseries)) - timeaverage*timeaverage
    metrics.append(timevariance)
    
    #4.is_quote_status
    '''
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['is_quote_status'] != False:
            x=x+1
    res=x/n
    metrics.append(res)
    '''
    
    #5.'time_zone'
    #time_11bool = False,time_10bool = False,time_9bool = False,time_8bool = False,time_7bool = False,time_6bool = False,time_5bool = False,time_4bool = False,time_3bool = False,time_2bool = False,time_1bool = False, time0bool = False, time1bool = False, time2bool = False, time3bool = False, time4bool = False, time5bool = False, time6bool = False, time7bool = False, time8bool = False, time9bool = False, time10bool = False, time11bool = False,time12bool = False, time13bool = False, time_230bool = False, time530bool = False, time630bool = False, time930bool = False
    timelist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #for i in range(31):
    #    timelist[i] = 0
    for tweet in tweetlist:
        time_zone = tweet['user']['time_zone'] 
        if time_zone in ["International Date Line West","Midway Island","Samoa"]:
            timelist[0] = timelist[0] + 1
        elif time_zone in ["Hawaii"]:
            timelist[1] = timelist[1] + 1
        elif time_zone in ["Alaska"]:
            timelist[2] = timelist[2] + 1
        elif time_zone in ["Pacific Time (US & Canada)","Tijuana","Arizona","Chihuahua","Mazatlan"]:
            timelist[3] = timelist[3] + 1
        elif time_zone in ["Mountain Time (US & Canada)","Saskachewan","Guadalajara","Mexico City","Monterrey","Central America"]:
            timelist[4] = timelist[4] + 1
        elif time_zone in ["Central Time (US & Canada","Bogota","Lima","Quito"]:
            timelist[5] = timelist[5] + 1
        elif time_zone in ["Eastern Time (US & Canada)","Indiana (East)","Caracas","La Paz","Georgetown"]:
            timelist[6] = timelist[6] + 1
        elif time_zone in ["Atlantic Time (Canada)","Santiago","Brasilia","Buenos Aires"]:
            timelist[7] = timelist[7] + 1
        elif time_zone in ["Newfoundland"]:
            timelist[8] = timelist[8] + 1
        elif time_zone in ["Greenland","Mid-Atlantic"]:
            timelist[9] = timelist[9] + 1
        elif time_zone in ["Cape Verde Is."]:
            timelist[10] = timelist[10] + 1
        elif time_zone in ["Azores","Monrovia","UTC"]:
            timelist[11] = timelist[11] + 1
        elif time_zone in ["Dublin","Edinburgh","London","Lisbon","Casablanca","West Central Africa"]:
            timelist[12] = timelist[12] + 1
        elif time_zone in ["Belgrade","Bratislava","Budapest","Ljubljana","Prague","Sarajevo","Skopje","Warsaw","Zagreb","Brussels","Copenhagen","Madrid","Paris","Amsterdam","Berlin","Bern","Rome","Stockholm","Vienna","Cairo","Harare","Pretoria"]:
            timelist[13] = timelist[13] + 1
        elif time_zone in ["Bucharest","Helsinki","Kiev","Kyiv","Riga","Sofia","Tallinn","Vilnius","Athens","Istanbul","Minsk","Jerusalem","Moscow","St. Petersburg","Volgograd","Kuwait","Riyadh","Nairobi","Baghdad"]:
            timelist[14] = timelist[14] + 1
        elif time_zone in ["Abu Dhabi","Muscat","Baku","Tbilisi","Yerevan"]:
            timelist[15] = timelist[15] + 1
        elif time_zone in ["Tehran","Kabul"]:
            timelist[16] = timelist[16] + 1
        elif time_zone in ["Ekaterinburg","Islamabad","Karachi","Tashkent"]:
            timelist[17] = timelist[17] + 1
        elif time_zone in ["Chennai","Kolkata","Mumbai","New Delhi","Sri Jayawardenepura"]:
            timelist[18] = timelist[18] + 1
        elif time_zone in ["Kathmandu"]:
            timelist[19] = timelist[19] + 1
        elif time_zone in ["Astana","Dhaka","Almaty","Urumqi"]:
            timelist[20] = timelist[20] + 1
        elif time_zone in ["Rangoon"]:
            timelist[21] = timelist[21] + 1
        elif time_zone in ["Novosibirsk","Bangkok","Hanoi","Jakarta","Krasnoyarsk"]:
            timelist[22] = timelist[22] + 1
        elif time_zone in ["Beijing","Chongqing","Hong Kong","Kuala Lumpur","Singapore","Taipei","Perth","Irkutsk","Ulaan Bataar"]:
            timelist[23] = timelist[23] + 1
        elif time_zone in ["Soeul","Osaka","Sapporo","Tokyo","Yakutsk"]:
            timelist[24] = timelist[24] + 1
        elif time_zone in ["Darwin"]:
            timelist[25] = timelist[25] + 1
        elif time_zone in ["Brisbane","Vladivostok","Guam","Port Moresby","Solomon Is."]:
            timelist[26] = timelist[26] + 1
        elif time_zone in ["Adelaide"]:
            timelist[27] = timelist[27] + 1
        elif time_zone in ["Canberra","Melbourne","Sydney","Hobart","Magadan","New Caledonia"]:
            timelist[28] = timelist[28] + 1
        elif time_zone in ["Fiji","Kamchatka","Marshall Is."]:
            timelist[29] = timelist[29] + 1
        elif time_zone in ["Auckland","Wellington","Nuku'alofa"]:
            timelist[30] = timelist[30] + 1
        
    numberofzones = 0
    for i in range(len(timelist)):
        if timelist[i] != 0:
            numberofzones = numberofzones + 1
    metrics.append(numberofzones)
    
    #time zone distribution
    outData['timeZoneDistribution'] = timelist
    
    #6.'time_zone_var'
    timezoneaverage = ((-11)*timelist[0] + (-10)*timelist[1] + (-8)*timelist[2] + (-7)*timelist[3] + (-6)*timelist[4] + (-5)*timelist[5] + (-4)*timelist[6] + (-3)*timelist[7] + (-2.5)*timelist[8] + (-2)*timelist[9] + (-1)*timelist[10] + timelist[12] + 2*timelist[13] + 3*timelist[14] + 4*timelist[15] + 4.5*timelist[16] + 5*timelist[17] + 5.5*timelist[18] + 5.75*timelist[19] + 6*timelist[20] + 6.5*timelist[21] + 7*timelist[22] + 8*timelist[23] + 9*timelist[24] + 9.5*timelist[25] + 10*timelist[26] + 10.5*timelist[27] + 11*timelist[28] + 12*timelist[29] + 13*timelist[30])/n
    timezonevar = ((121*timelist[0] + 100*timelist[1] + 64*timelist[2] + 49*timelist[3] + 36*timelist[4] + 25*timelist[5] + 16*timelist[6] + 9*timelist[7] + (2.5*2.5)*timelist[8] + 4*timelist[9] + timelist[10] + timelist[12] + 4*timelist[13] + 9*timelist[14] + 16*timelist[15] + (4.5*4.5)*timelist[16] + 25*timelist[17] + (5.5*5.5)*timelist[18] + (5.75*5.75)*timelist[19] + 36*timelist[20] + (6.5*6.5)*timelist[21] + 49*timelist[22] + 64*timelist[23] + 81*timelist[24] + (9.5*9.5)*timelist[25] + 100*timelist[26] + (10.5*10.5)*timelist[27] + 121*timelist[28] + 144*timelist[29] + 169*timelist[30])/n) - timezoneaverage*timezoneaverage
    metrics.append(timezonevar)
    
    #7.'has_extended_profile'
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['user']['has_extended_profile'] != False:
            x=x+1
    res=x/n
    metrics.append(res)
    
    #8.'default_profile'
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['user']['default_profile'] != False:
            x=x+1
    res=x/n
    metrics.append(res)
    
    #percentage of users with default_profile
    outData['usersWithDefaultProfile'] = res
    
    #9.'name_length_ave'
    totallength = 0
    for tweet in tweetlist:
        if tweet['user']['name'] != None:
            totallength = totallength + len(tweet['user']['name'])
    averagelength = totallength/n
    metrics.append(averagelength)
    
    #10.'created_at_ave_after_first_user'
    user_created = []
    for tweet in tweetlist:
       user_created.append(datetime.strptime(tweet['user']['created_at'], '%a %b %d %H:%M:%S %z %Y'))
    earliesttime = user_created[0]
    earliesttimeentry = 0
    for ct in user_created:
        if ct < earliesttime:
            earliesttime = ct
            earliesttimeentry = x
    #earliesttime is the tweet in this topic which was written first and earliesttimeentry is which entry this is found at
    timesum = 0
    timesumsquare = 0
    for x in user_created:
        difference = x - earliesttime
        differencenumber = (difference.days)*24*60*60 + difference.seconds
        timesum = timesum + differencenumber
        timesumsquare = timesumsquare + differencenumber*differencenumber
    timeaverage = timesum/n
    metrics.append(timeaverage)
    
    
    #11.'followers_count_ave'
    followers = []
    for tweet in tweetlist:
        followers.append(tweet['user']['followers_count'])
    av= np.mean(followers)
    metrics.append(av)
    
    #number of followers of users
    outData['followers'] = followers
    #average of number of followers 
    outData['aveFollowers'] = np.mean(followers)
    
    #12.'followers_count_var'
    va=np.var(followers)
    metrics.append(va)
    
    #variance of number of followers
    outData['varFollowers'] = va
    
    
    #13.'favourites_count_ave'
    favs = []
    for tweet in tweetlist:
        favs.append(tweet['user']['favourites_count'])
    av= np.mean(favs)
    metrics.append(av)
    
    #favorites count by users
    outData['userFavoritesCount'] = favs
    
    #14. 'screen_name_length_ave'
    totallength = 0
    totalsquare = 0
    for tweet in tweetlist:
        if tweet['user']['screen_name'] != None:
            totallength = totallength + len(tweet['user']['screen_name'])
            totalsquare = totalsquare + len(tweet['user']['screen_name'])*len(tweet['user']['screen_name'])
    averagelength = totallength/n
    metrics.append(averagelength)
    
    
    #15. 'screen_name_length_var'
    varlength = totalsquare/n - averagelength*averagelength
    metrics.append(varlength)
    
    #16. 'verified_no'
    x=0
    res=0.0
    tweets_by_verified = []
    verified_user = []
    for t in range(len(tweetlist)):
        if tweetlist[t]['user']['verified'] != False:
            x=x+1
            verified_user.append(tweet['user']['screen_name'])
            tweets_by_verified.append(tweets[t])
    res=x/n
    metrics.append(res)
    
    #tweets by verified user
    outData['tweetsByVerified'] = tweets_by_verified
    outData['verifiedUsers'] = verified_user
    
    
    #17.'friends_count_ave'
    f = []
    for tweet in tweetlist:
        f.append(tweet['user']['friends_count'])
    av= np.mean(f)
    metrics.append(av)
    
    outData['aveFriendCount'] = av
    outData['friendCounts'] = f
    
    #18.'friends_count_var'
    va=np.var(f)
    metrics.append(va)
    
    #19.'geo_enabled_true'
    '''
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['user']['geo_enabled'] != False:
            x=x+1
    res=x/n
    metrics.append(res)
    '''      
            
    #20. 'statuses_count_ave'
    s = []
    for tweet in tweetlist:
        s.append(tweet['user']['statuses_count'])
    av= np.mean(s)
    metrics.append(av)
    
    outData['aveStatusCount'] = av
    outData['statusCounts'] = s
    
    #21.'statuses_count_var'
    va=np.var(s)
    metrics.append(va)
    
    #22.'lang_non_English'
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['user']['lang'] != 'en':
            x=x+1
    res=x/n
    metrics.append(res)
            
            
    #23.'is_translation_enabled'
    '''
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['user']['is_translation_enabled']!= False:
            x=x+1
    res=x/n
    metrics.append(res)
    '''
    
    #24.'non_url_no'(!!NOT IN METRICS)
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['user']['url'] != None:
            x=x+1
    res=x/n
    #metrics.append(res)
    
    outData['percentageUsersWithUrl'] = res
    
    #25.'urls_no'
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['entities']['urls'] != []:
            x=x+1
    res=x/n
    metrics.append(res)
    
    outData['percentageTweetsWithUrl'] = res
    outData['tweetsWithUrl'] = x
    
            
    #26.'ave_hashtags'
    x=0
    #res=0.0
    total = 0
    for tweet in tweetlist:
        if tweet['entities']['hashtags'] != []:
            x=x+1
            total += len(tweet['entities']['hashtags'])
    #res=x/n
    #metrics.append(res)
    av = total/n
    metrics.append(av)
    outData['aveHashtagsInTweets'] = av
    
    #27.'ave_symbols'
    x=0
    res=0.0
    total = 0
    for tweet in tweetlist:
        if tweet['entities']['symbols'] != []:
            x=x+1
            total += len(tweet['entities']['symbols'])
    #res=x/n
    #metrics.append(res)
    av = total/n 
    outData['aveSymbolsInTweets'] = av
    
    #28.'favorite_count_ave'
    fav = []
    for tweet in tweetlist:
        fav.append(tweet['favorite_count'])
    av= np.mean(fav)
    metrics.append(av)
    
    outData['tweetsFavoriteCounts'] = fav
    outData['aveTweetsFavoriteCount'] = av
    
    #29.'favorite_count_var'
    va=np.var(fav)
    metrics.append(va)
    
    
    #30.'place_non_null'
    x=0
    res=0.0
    for tweet in tweetlist:
        if tweet['place'] != None:
            x=x+1
    res=x/n
    metrics.append(res)
    
    
    #31.'text_length_ave'
    totallength = 0
    posTweets = 0
    negTweets = 0
    tweetsSemaScore = []
    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweetlist:
        if tweet['text'] != None:
            totallength = totallength + len(tweet['text'])
            scores = analyzer.polarity_scores(tweet['text'])
            tweetsSemaScore.append(scores['compound'])
            if scores['compound'] > 0:
                posTweets = posTweets + 1
            elif scores['compound'] < 0:
                negTweets = negTweets + 1
        else:
            tweetsSemaScore.append(0)
    averagelength = totallength/n
    averageCompound = np.mean(tweetsSemaScore)
    compound_var = np.var(tweetsSemaScore)
    upperPercentile = np.percentile(tweetsSemaScore,75)
    lowerPercentile = np.percentile(tweetsSemaScore,25)
    tweetsWithStrongPos = []
    tweetsWithStrongNeg = []
    for i in range(len(tweetlist)):
        if tweetsSemaScore[i] > max(upperPercentile,0):
            tweetsWithStrongPos.append(tweetlist[i])
        elif tweetsSemaScore[i] < min(lowerPercentile, 0):
            tweetsWithStrongNeg.append(tweetlist[i])
    metrics.append(averagelength)
        
    
    #32.'retweet_count_ave'
    r = []
    for tweet in tweetlist:
        r.append(tweet['retweet_count'])
    av= np.mean(r)
    metrics.append(av)
    
    outData['aveRetweetCount'] = av
    outData['retweetCounts'] = r
    
    #33.'retweet_count_var'
    va=np.var(r)
    metrics.append(va)
    
    #34,35. semantic analysis
    metrics.append(averageCompound)
    metrics.append(compound_var)
    outData['semanticScores'] = tweetsSemaScore
    outData['percentagePosTweets'] = posTweets/n
    outData['percentageNegTweets'] = negTweets/n
    outData['strongPosTweets'] = tweetsWithStrongPos
    outData['strongNegTweets'] = tweetsWithStrongNeg
    outData['aveSemaScore'] = averageCompound
    outData['varSemaScore'] = compound_var
    
    
    '''
    metrics:
       0.'in_reply_to_status_id_str',
       1.'created_at_ave_after_first_time', 2.'created_at_var', 
       ###3.'is_quote_status',
       4.'time_zone', 5.'time_zone_var', 
       6.'has_extended_profile', 7.'default_profile',
       8.'name_length_ave', 9.'created_at_ave_after_first_user',
       10.'followers_count_ave',11.'followers_count_var',
       12.'favourites_count_ave',
       13.'screen_name_length_ave', 14.'screen_name_length_var', 
       15.'verified_no',
       16.'friends_count_ave', 17.'friends_count_var', 
       ###18.'geo_enabled_true',
       19.'statuses_count_ave', 20.'statuses_count_var',21.'user_lang_non_English',
       ###22.'is_translation_enabled', ###23.'non_url_no',
       24.'urls_no',
       25.'ave_hashtags', ###26.'symbols_no', 
       27.'favorite_count_ave',28.'favorite_count_var',
       29.'place_non_null', 30.'text_length_ave',
       31.'retweet_count_ave',32.'retweet_count_var'
       33.'compound', 34.'compound_var'
     '''
     
    
    #some additional data just for presenting:
    
    #reply count
    r = []
    for tweet in tweetlist:
        r.append(tweet['retweet_count'])
    av= np.mean(r)
    outData['replyCounts'] = r
    outData['avReplyCount'] = av
    
    #coordinates
    c = []
    for tweet in tweetlist:
        if tweet['coordinates'] != None:
            c.append(tweet['coordinates'])
    outData['tweetsCoordinates'] = c
    
    #calculate credibility score
    data_scaled_normal = normalizer.transform(scaler.transform(np.array(metrics).reshape(1,-1)))
    #print(data_scaled_normal)
    score = lclf.predict([data_scaled_normal][0])
    #print(score)
    score = round(min(max((score[0]+2)/4 * 100, 0), 100))
    
    #output dictionary
    outData['credScore'] = score 
    return outData
    

