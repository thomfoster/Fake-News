import csv, json, sys
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timezone
import itertools
import ast

def computeFeatures(INPUT_FILE):
    overalllist=[]
    #INPUT_FILE = 'tweets0.csv'
    rownumber=0
    metriclist = ['in_reply_to_status_id_str','contributors','coordinates','retweeted','created_at','truncated','is_quote_status','user','favorited','in_reply_to_user_id_str','entities','favorite_count','lang','in_reply_to_user_id','place','text','geo','retweet_count']
    userlist = ['translator_type','time_zone','follow_request_sent','profile_text_color','has_extended_profile','utc_offset','contributors_enabled','default_profile','name','created_at','profile_background_color','followers_count','description','favourites_count','screen_name','verified','profile_sidebar_border_color','friends_count','default_profile_image','geo_enabled','profile_use_background_image','profile_background_tile','entities','statuses_count','lang','protected','profile_link_color','is_translation_enabled','url']
    #need something special for [user][entities] and I had to remove 'profile_banner_url' because it was missing from some random fields, I told Andrei about that
    entitieslist = ['user_mentions','urls','hashtags','symbols']
    #user and entities both have subfields so these are separate cases
    
    #csv.field_size_limit(sys.maxsize)
    with open(INPUT_FILE, 'r', newline='\n') as csvfile:
        tweet_reader = csv.reader(csvfile, dialect='excel', quotechar='\"')
        for row in tweet_reader:
            rownumber=rownumber+1
            subject_read = False
            subject = ""
            tweets = []
            for col in row:
                # Avoid the first 
                if subject_read:
                    tweets.append(json.loads(col))
                else:
                    subject = col
                    subject_read = True  
                    topictitle = col  
            #each tweet is still a cell, we want to convert to a list of list of metrics with all (for example) coordinates in a list in one cell
            
            m=0
            listoflists = []
            #make a list with one empty list for each metric which we will add to
            for k in range(49):
                listoflists.append([])
            #this loop runs through each metric and takes the right field from each tweet in the row
            while m<49:
                for l in range(len(metriclist)):
    
                    if metriclist[l] == 'user':
                        for n in range(len(userlist)):
                                for i in range(len(tweets)):
                                    if tweets[i] != {}:
                                        (listoflists[m+n]).append(tweets[i]['user'][userlist[n]])
                        m=m+n
                    elif (metriclist[l]=='entities'):
                        for p in range(len(entitieslist)):
                                for j in range(len(tweets)):
                                    if tweets[j] != {}:
                                        (listoflists[m+p]).append(tweets[j]['entities'][entitieslist[p]])
                        m=m+p
                    else:
                        for o in range(len(tweets)):
                                if tweets[o] != {}:
    
                                    (listoflists[m]).append(tweets[o][metriclist[l]])
                    m=m+1
    
    
            #adds to topic title to the front of the list of metrics for the topic
            listoflists.insert(0,topictitle)
    
    
            listofmetrics=[]
            #     0. topictitle
            listofmetrics.append(topictitle)
            lm=1
            #for each metric we'll manually count everything
            #     1. in_reply_to_status_id_str #
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
    
            #     2. contributors #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     3. coordinates #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
    
            #     4. retweeted #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     5. created_at average after first time
            lm=lm+1
            #change dates and times into standard format
            for x in range(len(listoflists[lm])):
                listoflists[lm][x] = datetime.strptime(listoflists[lm][x], '%a %b %d %H:%M:%S %z %Y')
            earliesttime = listoflists[lm][0]
            earliesttimeentry = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] < earliesttime:
                    earliesttime = listoflists[lm][x]
                    earliesttimeentry = x
            #earliesttime is the tweet in this topic which was written first and earliesttimeentry is which entry this is found at
            timesum = 0
            timesumsquare = 0
            for x in range(len(listoflists[lm])):
                difference = listoflists[lm][x] - earliesttime
                differencenumber = (difference.days)*24*60*60 + difference.seconds
                timesum = timesum + differencenumber
                timesumsquare = timesumsquare + differencenumber*differencenumber
            timeaverage = timesum/len(listoflists[lm]) 
            listofmetrics.append(timeaverage)   
            #     6. created_at Variance 
            #lm only once, because we're using the same metric
            timevariance = ((timesumsquare)/len(listoflists[lm])) - timeaverage*timeaverage
            listofmetrics.append(timevariance)
    
            #     8. Truncated #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     9. is_quote_status #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
    
            #     11. translator_type #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     13. time_zone # of timezones
            lm=lm+1
            #time_11bool = False,time_10bool = False,time_9bool = False,time_8bool = False,time_7bool = False,time_6bool = False,time_5bool = False,time_4bool = False,time_3bool = False,time_2bool = False,time_1bool = False, time0bool = False, time1bool = False, time2bool = False, time3bool = False, time4bool = False, time5bool = False, time6bool = False, time7bool = False, time8bool = False, time9bool = False, time10bool = False, time11bool = False,time12bool = False, time13bool = False, time_230bool = False, time530bool = False, time630bool = False, time930bool = False
            timelist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            #for i in range(31):
            #    timelist[i] = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] in ["International Date Line West","Midway Island","Samoa"]:
                     timelist[0] = timelist[0] + 1
                elif listoflists[lm][x] in ["Hawaii"]:
                    timelist[1] = timelist[1] + 1
                elif listoflists[lm][x] in ["Alaska"]:
                    timelist[2] = timelist[2] + 1
                elif listoflists[lm][x] in ["Pacific Time (US & Canada)","Tijuana","Arizona","Chihuahua","Mazatlan"]:
                    timelist[3] = timelist[3] + 1
                elif listoflists[lm][x] in ["Mountain Time (US & Canada)","Saskachewan","Guadalajara","Mexico City","Monterrey","Central America"]:
                    timelist[4] = timelist[4] + 1
                elif listoflists[lm][x] in ["Central Time (US & Canada","Bogota","Lima","Quito"]:
                    timelist[5] = timelist[5] + 1
                elif listoflists[lm][x] in ["Eastern Time (US & Canada)","Indiana (East)","Caracas","La Paz","Georgetown"]:
                    timelist[6] = timelist[6] + 1
                elif listoflists[lm][x] in ["Atlantic Time (Canada)","Santiago","Brasilia","Buenos Aires"]:
                    timelist[7] = timelist[7] + 1
                elif listoflists[lm][x] in ["Newfoundland"]:
                    timelist[8] = timelist[8] + 1
                elif listoflists[lm][x] in ["Greenland","Mid-Atlantic"]:
                    timelist[9] = timelist[9] + 1
                elif listoflists[lm][x] in ["Cape Verde Is."]:
                    timelist[10] = timelist[10] + 1
                elif listoflists[lm][x] in ["Azores","Monrovia","UTC"]:
                    timelist[11] = timelist[11] + 1
                elif listoflists[lm][x] in ["Dublin","Edinburgh","London","Lisbon","Casablanca","West Central Africa"]:
                    timelist[12] = timelist[12] + 1
                elif listoflists[lm][x] in ["Belgrade","Bratislava","Budapest","Ljubljana","Prague","Sarajevo","Skopje","Warsaw","Zagreb","Brussels","Copenhagen","Madrid","Paris","Amsterdam","Berlin","Bern","Rome","Stockholm","Vienna","Cairo","Harare","Pretoria"]:
                    timelist[13] = timelist[13] + 1
                elif listoflists[lm][x] in ["Bucharest","Helsinki","Kiev","Kyiv","Riga","Sofia","Tallinn","Vilnius","Athens","Istanbul","Minsk","Jerusalem","Moscow","St. Petersburg","Volgograd","Kuwait","Riyadh","Nairobi","Baghdad"]:
                    timelist[14] = timelist[14] + 1
                elif listoflists[lm][x] in ["Abu Dhabi","Muscat","Baku","Tbilisi","Yerevan"]:
                    timelist[15] = timelist[15] + 1
                elif listoflists[lm][x] in ["Tehran","Kabul"]:
                    timelist[16] = timelist[16] + 1
                elif listoflists[lm][x] in ["Ekaterinburg","Islamabad","Karachi","Tashkent"]:
                    timelist[17] = timelist[17] + 1
                elif listoflists[lm][x] in ["Chennai","Kolkata","Mumbai","New Delhi","Sri Jayawardenepura"]:
                    timelist[18] = timelist[18] + 1
                elif listoflists[lm][x] in ["Kathmandu"]:
                    timelist[19] = timelist[19] + 1
                elif listoflists[lm][x] in ["Astana","Dhaka","Almaty","Urumqi"]:
                    timelist[20] = timelist[20] + 1
                elif listoflists[lm][x] in ["Rangoon"]:
                    timelist[21] = timelist[21] + 1
                elif listoflists[lm][x] in ["Novosibirsk","Bangkok","Hanoi","Jakarta","Krasnoyarsk"]:
                    timelist[22] = timelist[22] + 1
                elif listoflists[lm][x] in ["Beijing","Chongqing","Hong Kong","Kuala Lumpur","Singapore","Taipei","Perth","Irkutsk","Ulaan Bataar"]:
                    timelist[23] = timelist[23] + 1
                elif listoflists[lm][x] in ["Soeul","Osaka","Sapporo","Tokyo","Yakutsk"]:
                    timelist[24] = timelist[24] + 1
                elif listoflists[lm][x] in ["Darwin"]:
                    timelist[25] = timelist[25] + 1
                elif listoflists[lm][x] in ["Brisbane","Vladivostok","Guam","Port Moresby","Solomon Is."]:
                    timelist[26] = timelist[26] + 1
                elif listoflists[lm][x] in ["Adelaide"]:
                    timelist[27] = timelist[27] + 1
                elif listoflists[lm][x] in ["Canberra","Melbourne","Sydney","Hobart","Magadan","New Caledonia"]:
                    timelist[28] = timelist[28] + 1
                elif listoflists[lm][x] in ["Fiji","Kamchatka","Marshall Is."]:
                    timelist[29] = timelist[29] + 1
                elif listoflists[lm][x] in ["Auckland","Wellington","Nuku'alofa"]:
                    timelist[30] = timelist[30] + 1
        
            numberofzones = 0
            for i in range(len(timelist)):
                if timelist[i] != 0:
                    numberofzones = numberofzones + 1
            listofmetrics.append(numberofzones)
    
            #     14. time_zone average
            timezoneaverage = ((-11)*timelist[0] + (-10)*timelist[1] + (-8)*timelist[2] + (-7)*timelist[3] + (-6)*timelist[4] + (-5)*timelist[5] + (-4)*timelist[6] + (-3)*timelist[7] + (-2.5)*timelist[8] + (-2)*timelist[9] + (-1)*timelist[10] + timelist[12] + 2*timelist[13] + 3*timelist[14] + 4*timelist[15] + 4.5*timelist[16] + 5*timelist[17] + 5.5*timelist[18] + 5.75*timelist[19] + 6*timelist[20] + 6.5*timelist[21] + 7*timelist[22] + 8*timelist[23] + 9*timelist[24] + 9.5*timelist[25] + 10*timelist[26] + 10.5*timelist[27] + 11*timelist[28] + 12*timelist[29] + 13*timelist[30])/len(listoflists[lm])
            listofmetrics.append(timezoneaverage)
            #     15. time_zone Variance
            timezonevar = ((121*timelist[0] + 100*timelist[1] + 64*timelist[2] + 49*timelist[3] + 36*timelist[4] + 25*timelist[5] + 16*timelist[6] + 9*timelist[7] + (2.5*2.5)*timelist[8] + 4*timelist[9] + timelist[10] + timelist[12] + 4*timelist[13] + 9*timelist[14] + 16*timelist[15] + (4.5*4.5)*timelist[16] + 25*timelist[17] + (5.5*5.5)*timelist[18] + (5.75*5.75)*timelist[19] + 36*timelist[20] + (6.5*6.5)*timelist[21] + 49*timelist[22] + 64*timelist[23] + 81*timelist[24] + (9.5*9.5)*timelist[25] + 100*timelist[26] + (10.5*10.5)*timelist[27] + 121*timelist[28] + 144*timelist[29] + 169*timelist[30])/len(listoflists[lm])) - timezoneaverage*timezoneaverage
            listofmetrics.append(timezonevar)
            #     16. follow_request_sent #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     17. profile_text_color #
            lm=lm+1
            default = 0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != "333333":
                    default = default + 1
            per = default/len(listoflists[lm])
            listofmetrics.append(per)
            #     18. has_extended_profile #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     19. utc_offset average
            lm=lm+1
            utcoffset = 0
            nonnull = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != None:
                    utcoffset = utcoffset + listoflists[lm][x]
                    nonnull = nonnull + 1
            if nonnull == 0:
                listofmetrics.append(None)
            else:
                average = utcoffset/nonnull
                listofmetrics.append(average)
    
            #     20. contributors_enabled #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     21. default_profile #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     22. average name length
            lm=lm+1
            totallength = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != None:
                    totallength = totallength + len(listoflists[lm][x])
            averagelength = totallength/len(listoflists[lm])
            listofmetrics.append(averagelength)
            #     23. created_at average after first user
            lm=lm+1
            for x in range(len(listoflists[lm])):
                listoflists[lm][x] = datetime.strptime(listoflists[lm][x], '%a %b %d %H:%M:%S %z %Y')
            earliesttime = listoflists[lm][0]
            earliesttimeentry = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] < earliesttime:
                    earliesttime = listoflists[lm][x]
                    earliesttimeentry = x
            #earliesttime is the tweet in this topic which was written first and earliesttimeentry is which entry this is found at
            timesum = 0
            timesumsquare = 0
            for x in range(len(listoflists[lm])):
                difference = listoflists[lm][x] - earliesttime
                differencenumber = (difference.days)*24*60*60 + difference.seconds
                timesum = timesum + differencenumber
                timesumsquare = timesumsquare + differencenumber*differencenumber
            timeaverage = timesum/len(listoflists[lm]) 
            listofmetrics.append(timeaverage)
            #     24. profile_background_color #
            lm=lm+1
            default = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != "C0DEED":
                    default = default + 1
            per = default/len(listoflists[lm])
            listofmetrics.append(per)
    
            #     25. followers_count average
            lm=lm + 1
            av=np.mean(listoflists[lm])
            listofmetrics.append(av)
            
            #     26. followers_count variance
            va=np.var(listoflists[lm])
            listofmetrics.append(va)
            
            #     27. Description #
            lm=lm+1
            totallength = 0
            desc = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != None:
                    desc = desc + 1
                    totallength = totallength + len(listoflists[lm][x])
            averagelength = totallength/len(listoflists[lm])
            perdesc = desc/len(listoflists[lm])
            listofmetrics.append(perdesc)
            #     28. Description average length
            listofmetrics.append(averagelength)
           
            #     29. favourites_count average
            lm=lm+1
            av=np.mean(listoflists[lm])
            listofmetrics.append(av)
            
            #     30. favourites_count variance
            va=np.var(listoflists[lm])
            listofmetrics.append(va)
            
            #     31. screen_name average length
            lm=lm+1
            totallength = 0
            totalsquare = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != None:
                    totallength = totallength + len(listoflists[lm][x])
                    totalsquare = totalsquare + len(listoflists[lm][x])*len(listoflists[lm][x])
            averagelength = totallength/len(listoflists[lm])
            listofmetrics.append(averagelength)
            #     32. screen_name variance of length
            varlength = totalsquare/len(listoflists[lm]) - averagelength*averagelength
            listofmetrics.append(varlength)
           
            #     33. Verified #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     34. profile_sidebar_border_color #
            lm=lm+1
            default = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != "C0DEED":
                    default = default + 1
            per = default/len(listoflists[lm])
            listofmetrics.append(per)
    
            #     35. friends_count average
            lm=lm+1
            av=np.mean(listoflists[lm])
            listofmetrics.append(av)
            
            #     36. friends_count variance
            va=np.var(listoflists[lm])
            listofmetrics.append(va)
            
    
            #     38. default_profile_image # of false
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] == False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     39. geo_enabled # true
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
    
            #     41. profile_use_background_image #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     42. profile_background_tile #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     43. Entities (do we want to do this stuff?)
            lm=lm+1
            #     44. statuses_count average
            lm=lm + 1
            av=np.mean(listoflists[lm])
            listofmetrics.append(av)
            
            #     45. statuses_count variance
            va=np.var(listoflists[lm])
            listofmetrics.append(va)
            
            #     47. Lang # non-English
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != 'en':
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     48. Protected #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     49. profile_link_color #
            lm=lm+1
            default = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != "1DCAFF":
                    default = default + 1
            per = default/len(listoflists[lm])
            listofmetrics.append(per)
            
            #     50. is_translation_enabled #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     51. Url # non-null
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     52. Favorited #
            lm=lm+1
            """
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != False:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            """
            
            #     53. in_reply_to_user_id_str # non-null
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     54. user_mentions #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != []:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     55. Urls #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != []:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     56. Hashtags #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != []:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     57. Symbols #
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != []:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     58. favorite_count average
            lm=lm+1
            av=np.mean(listoflists[lm])
            listofmetrics.append(av)
            
            #     59. favorite_count variance
            va=np.var(listoflists[lm])
            listofmetrics.append(va)
    
            #     60. Lang # non-english
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != 'en':
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     62. in_reply_to_user_id # non-null
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     63. Place # non-null
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            
            #     64. Text average length
            lm=lm+1
            totallength = 0
            totalsquare = 0
            for x in range(len(listoflists[lm])):
                if listoflists[lm][x] != None:
                    totallength = totallength + len(listoflists[lm][x])
                    totalsquare = totalsquare + len(listoflists[lm][x])*len(listoflists[lm][x])
            averagelength = totallength/len(listoflists[lm])
            listofmetrics.append(averagelength)
    
            #     65. Geo
            lm=lm+1
            x=0
            res=0.0
            for i in range(len(listoflists[lm])):
                if listoflists[lm][i] != None:
                    x=x+1
            res=x/len(listoflists[lm])
            listofmetrics.append(res)
            #     66. retweet_count average
            lm=lm+1
            av=np.mean(listoflists[lm])
            listofmetrics.append(av)
            
            #     67. retweet_count variance
            va=np.var(listoflists[lm])
            listofmetrics.append(va)
            
    
            overalllist.append(listofmetrics)
            #print('rows read',len(overalllist))
    return overalllist





#iterate over files
#inputfiles = ['tweets0.csv','tweets1.csv','tweets2.csv','tweets3.csv','tweets4.csv','tweets5.csv','tweets6.csv','tweets7.csv','tweets8.csv','tweets9.csv']

def readFiles(tweetsfiles, credfile):
    """
    featurelist = ['topic_title','in_reply_to_status_id_str','contributors','coordinates','retweeted','created_at_ave_after_first_time','created_at_var','truncated','is_quote_status','translator_type','time_zone','time_zone_ave','time_zone_var','follow_request_sent','profile_text_color','has_extended_profile','utc_offset_ave','contributors_enabled',
                   'default_profile','name_length_ave','created_at_ave_after_first_user','profile_background_color','followers_count_ave','followers_count_var','description_no','description_length_ave','favourites_count_ave','favourites_count_var','screen_name_length_ave','screen_name_length_var','verified_no','profile_sidebar_border_color','friends_count_ave','friends_count_var','default_profile_image_false','geo_enabled_true','profile_use_background_image',
                   'profile_background_tile','statuses_count_ave','statuses_count_var','tweets_lang_non_English','protected_no','profile_link_color','is_translation_enabled','non_url_no','favorited_no','in_reply_to_user_id_str_non-null','user_mentions_no','urls_no',
                   'hashtags_no','symbols_no','favorite_count_ave','favorite_count_var','user_lang_non_english','in_reply_to_user_id_non-null','place_non_null','text_length_ave','geo','retweet_count_ave','retweet_count_var']
    """
    
    featurelist = ['topic_title','in_reply_to_status_id_str','coordinates','created_at_ave_after_first_time','created_at_var','is_quote_status','time_zone','time_zone_ave','time_zone_var',
                   'profile_text_color','has_extended_profile','utc_offset_ave',
                   'default_profile','name_length_ave','created_at_ave_after_first_user','profile_background_color',
                   'followers_count_ave','followers_count_var','description_no','description_length_ave','favourites_count_ave','favourites_count_var','screen_name_length_ave','screen_name_length_var',
                   'verified_no','profile_sidebar_border_color','friends_count_ave','friends_count_var','default_profile_image_false','geo_enabled_true','profile_use_background_image',
                   'profile_background_tile','statuses_count_ave','statuses_count_var','tweets_lang_non_English','profile_link_color','is_translation_enabled','non_url_no','in_reply_to_user_id_str_non-null','user_mentions_no','urls_no',
                   'hashtags_no','symbols_no','favorite_count_ave','favorite_count_var','user_lang_non_english','in_reply_to_user_id_non-null','place_non_null','text_length_ave','geo','retweet_count_ave','retweet_count_var']
    
    alllists = []
    for file in tweetsfiles:
        alllists = alllists + computeFeatures(file)
        print(file + 'file read')
    
    df = pd.DataFrame(alllists, columns = featurelist)
    df = df.set_index('topic_title')
    
    
    with open(credfile, 'r',encoding ='utf-8') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', quotechar='\"')
        list0 = []
        for row in reader:
            topic = []
            
            x = ast.literal_eval(row[2])
            sum = 0
            for i in x:
                sum = sum + int(i)
            
            ave = sum/len(x)
            topic.append(row[0])
            topic.append(ave)
            
            list0.append(topic)
            
    creddf = pd.DataFrame(list0, columns = ['topic_title','score'])
    creddf = creddf.set_index('topic_title')
    
    result = pd.concat([df, creddf], axis=1)         
    result = result.dropna(axis = 0)
    return result
