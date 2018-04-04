#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 16:35:59 2018

@author: cloverye
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import datasetComputation as dc


inputfiles = ['tweets0.csv','tweets1.csv','tweets2.csv','tweets3.csv','tweets4.csv','tweets5.csv','tweets6.csv','tweets7.csv','tweets8.csv','tweets9.csv']
credfile = 'cred.csv'

data = dc.readFiles(inputfiles, credfile)


#data analysis for machine learning
statistic = data.describe()
statistic.to_csv('statistic.csv')

"""
columns that has the same entry for all rows:
['contributors','retweeted','truncated','translator_type','follow_request_sent',
 'contributors_enabled','protected_no','favorited_no','description_no']
"""

"""
columns that are deleted due to meaningless data:
['contributors','retweeted','truncated','translator_type','follow_request_sent',
 'contributors_enabled','protected_no','favorited_no','description_no']   
"""

"""
features:
    in_reply_to_status_id_str: percentage of tweets being a reply
    ###retweeted: percentage of tweets that are NOT retweeted by the authenticating user
    created_at_after_first_time_ave
    created_at_var
    ###truncated
    is_quote_status: percentage of tweets that is NOT a Quoted Tweet. Example:
    ###translator_type
    time_zone: number of differrent time zones of tweets
    time_zone_ave
    time_zone_var
    
    ###follow_request_sent
    ###profile_text_color
    has_extended_profile
    # utc_offset_ave: average offset from GMT/UTC in seconds of authors
    ### contributors_enabled
    default_profile
    name_length_ave
    created_at_ave_after_first_user: average length of time between authors' first post and the tweets
    ###...profile_background_color: number of authors with profile background color not being default
    followers_count_ave: average number of followers of authors of tweets
    followers_count_var: varience of numbers of followers of authors of tweets
    ### description_no: percentage of tweets with an author with null description
    ### description_length_ave: average length of description of authors of tweets
    favourites_count_ave: average number of tweets authors has liked in the account’s lifetime
    favourites_count_var: varience of number of tweets authors has liked in the account's lifetime
    screen_name_length_ave: average length of screen name of authors
    screen_name_length_var: varience of length of screen names of authors
    verified_no: percentage of tweets whose author has a verified account
    ###...profile_sidebar_border_color
    friends_count_ave: average number of friends of authors
    friends_count_var: varience of number of friends of authors
    ###...default_profile_image_false
    geo_enabled_true: percentage of authors who has enabled the possibility of geotagging their Tweets
    ###...profile_use_background_image
    ###...profile_background_tile
    statuses_count_ave: average number of Tweets (including retweets) issued by the authors
    statuses_count_var: varience of number of tweets issued by the authors
    
    tweets_lang_non_English
    ###protected_no: percentage of author who has chosen to protect their Tweets
    ###...profile_link_color
    is_translation_enabled
    non_url_no:  percentage of authors that has A URL provided in association with their profile
    
    ### favorited_no: percentage of tweets that have been liked by the authenticating user
    ### in_reply_to_user_id_str_non-null
    user_mentions_no: percentage of tweets that contain user mentions
    urls_no: percentage of tweets that contain urls
    hashtags_no: percentage of tweets that contain hashtags
    symbols_no: percentage of tweets that contain symbols
    favorite_count_ave: average number of times Tweets have been liked by Twitter users
    favorite_count_var: varience of number of times tweets have been liked by Twitter users
    user_lang_non_english: percentage of non-english authors
    ### in_reply_to_user_id_non-null: percentage of tweets that is a reply
    place_non_null: percentage of tweets that has a place associated
    text_length_ave: average length of text
    geo: percentage of tweets that have geo info
    retweet_count_ave
    retweet_count_var
"""

#average several related columns: 'profile_background_tile','profile_text_color','profile_background_color','profile_sidebar_border_color','profile_link_color','description_no','profile_use_background_image','default_profile_image_false'
data['changed_profile'] = data.loc[:,['profile_background_tile','profile_text_color','profile_background_color','profile_sidebar_border_color','profile_link_color','profile_use_background_image','default_profile_image_false']].apply(np.mean, axis=1)

def adjust(x):
    return (x-(-2))/4 * 100

data['adjust_score'] = data.loc[:,'score'].apply(lambda x: (x-(-2))/4 * 100)
data.to_csv('twitter_topic_cred.csv')
#===========any change to the dataset is made above ================

#data analysis
cor = data.corr()
cor.to_csv('correlations.csv')

"""
plt.matshow(data.corr())
plt.xticks(range(len(data.columns)), data.columns)
plt.yticks(range(len(data.columns)), data.columns)
plt.colorbar()
plt.show()
"""
"""
related pairs:
    in_reply_to_status_id_str
    in_reply_to_user_id_str_non-null
    in_reply_to_user_id_non-null
    
    coordinates
    place_non_null
    geo
    
    time_zone_ave
    utc_offset_ave
    
    profile_text_color
    profile_background_color
    profile_sidebar_border_color
    profile_link_color
    
"""
"""
scores = data['score'].values
#in_reply_to_status_id_str
x = data['in_reply_to_status_id_str'].values
plt.scatter(x, scores, alpha=0.5)

x = data['coordinates'].values
plt.scatter(x, scores, alpha=0.5)

x = data['created_at_ave_after_first_time'].values
plt.scatter(x, scores, alpha=0.5)

x = data['is_quote_status'].values
plt.scatter(x, scores, alpha=0.5)

x = data['time_zone'].values
plt.scatter(x, scores, alpha=0.5)

x = data['time_zone_ave'].values
plt.scatter(x, scores, alpha=0.5)
"""

#===============data preprocessing========================================
from sklearn import preprocessing
"""
x_data = data.loc[:,['in_reply_to_status_id_str', 'coordinates',
       'created_at_ave_after_first_time', 'created_at_var', 'is_quote_status',
       'time_zone', 'time_zone_ave', 'time_zone_var', 'profile_text_color',
       'has_extended_profile', 'utc_offset_ave', 'default_profile',
       'name_length_ave', 'created_at_ave_after_first_user',
       'profile_background_color', 'followers_count_ave',
       'followers_count_var', 'description_no', 'description_length_ave',
       'favourites_count_ave', 'favourites_count_var',
       'screen_name_length_ave', 'screen_name_length_var', 'verified_no',
       'profile_sidebar_border_color', 'friends_count_ave',
       'friends_count_var', 'default_profile_image_false', 'geo_enabled_true',
       'profile_use_background_image', 'profile_background_tile',
       'statuses_count_ave', 'statuses_count_var', 'tweets_lang_non_English',
       'profile_link_color', 'is_translation_enabled', 'non_url_no',
       'in_reply_to_user_id_str_non-null', 'user_mentions_no', 'urls_no',
       'hashtags_no', 'symbols_no', 'favorite_count_ave', 'favorite_count_var',
       'user_lang_non_english', 'in_reply_to_user_id_non-null',
       'place_non_null', 'text_length_ave', 'geo', 'retweet_count_ave',
       'retweet_count_var','changed_profile']]
"""

x_data = data.loc[:,['in_reply_to_status_id_str',
       'created_at_ave_after_first_time', 'created_at_var', 
       'is_quote_status',
       'time_zone', 'time_zone_var', 
       'has_extended_profile', 'default_profile',
       'name_length_ave', 'created_at_ave_after_first_user',
       'followers_count_ave','followers_count_var',
       'favourites_count_ave',
       'screen_name_length_ave', 'screen_name_length_var', 'verified_no',
       'friends_count_ave','friends_count_var', 
       'geo_enabled_true',
       'statuses_count_ave', 'statuses_count_var', 'tweets_lang_non_English',
       'is_translation_enabled', 'non_url_no','urls_no',
       'hashtags_no', 'symbols_no', 
       'favorite_count_ave','favorite_count_var',
       'place_non_null', 'text_length_ave',
       'retweet_count_ave','retweet_count_var'
       #,'changed_profile'
       ]]


y_data = data.loc[:,'score']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)

#standardizing
scaler = preprocessing.StandardScaler().fit(x_train)
x_train_scaled = scaler.transform(x_train) 
x_test_scaled = scaler.transform(x_test)

#normalizing
normalizer = preprocessing.Normalizer().fit(x_train_scaled)
x_train_scaled_normal = normalizer.transform(x_train_scaled) 
x_test_scaled_normal = normalizer.transform(x_test_scaled) 

#=================fit model ================================================
#linear regression
from sklearn import datasets, linear_model
lm = linear_model.LinearRegression()
lm_model = lm.fit(x_train_scaled_normal, y_train)
y_scored = lm.predict(x_test_scaled_normal)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, y_scored)

#stocastic gradient decent
lm = linear_model.SGDRegressor()
lm_model = lm.fit(x_train_scaled_normal, y_train)
y_scored = lm.predict(x_test_scaled_normal)

mean_absolute_error(y_test, y_scored)

#support vector machine
from sklearn import svm
clf = svm.SVR()
clf.fit(x_train_scaled_normal, y_train)
y_scored = clf.predict(x_test_scaled_normal)
#clf.score(x_test_scaled_normal, y_test)
mean_absolute_error(y_test, y_scored)


#linear kernel support vector machine
from sklearn import svm
lclf = svm.SVR(kernel = 'linear')
lclf.fit(x_train_scaled_normal, y_train)
y_scored = lclf.predict(x_test_scaled_normal)
#lclf.score(x_test_scaled_normal, y_test)
mean_absolute_error(y_test, y_scored)


#decision tree
from sklearn import tree
clf = tree.DecisionTreeRegressor()
clf = clf.fit(x_train_scaled, y_train)
y_scored = clf.predict(x_test_scaled)
clf.score(x_test_scaled_normal, y_test)
mean_absolute_error(y_test, y_scored)

#neural network
from sklearn import neural_network
mlp = neural_network.MLPRegressor(alpha= 0.001, max_iter = 1000)
mlp = mlp.fit(x_train_scaled, y_train)
y_scored = clf.predict(x_test_scaled)

mean_absolute_error(y_test, y_scored)

## The line / model
plt.scatter(y_test, y_scored)
plt.xlabel("True Values")
plt.ylabel("score")
