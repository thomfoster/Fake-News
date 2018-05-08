from flask import Markup

def url_from_form(form_data):
    return "-".join(form_data.split())

def readable_from_url(url):
    return " "+" ".join(url.split('-'))

def get_credentials():
    with open('credentials.txt', 'r') as cred_file:
        contents = cred_file.read().split('\n')
        return (contents[0], contents[1])

def format_for_time_chart(data):
    creationTimes = data['creationTimes']
    creationTimes = list(map(lambda x: x.split('+')[0].split('T'), creationTimes))
    counts = dict()
    for dt in creationTimes:
        counts[dt[0] + ' at ' + dt[1][:2] + ':00'] = 0
    for dt in creationTimes:
        counts[dt[0] + ' at ' + dt[1][:2] + ':00'] += 1
    # chart js requires 2 seperate ordered lists
    labels = []
    values = []
    counts = sorted(counts.items())
    previous_date = counts[0][0].split(' at ')[0]
    labels.append(previous_date)
    values.append(counts[0][1])
    for (k,v) in counts[1:]:
        date = k.split(' at ')[0]
        if (previous_date == date):
            labels.append('')
        else:
            labels.append(date)
            previous_date = date
        values.append(v)
    if (len(values)>5):
        return [labels, values, len(labels)]
    # Group by hour
    counts = dict()
    for dt in creationTimes:
        counts[dt[0] + ' at ' + dt[1][:4]] = 0
    for dt in creationTimes:
        counts[dt[0] + ' at ' + dt[1][:4]] += 1
    counts = sorted(counts.items())
    labels = []
    values = []
    previous_date = counts[0][0].split(' at ')[0]
    labels.append(previous_date)
    values.append(counts[0][1])
    for (k,v) in counts[1:]:
        # if (v == 0):
        #     continue
        date = k.split(' at ')[0]
        if (previous_date == date):
            labels.append('')
        else:
            labels.append(k)
            previous_date = date
        values.append(v)
    return [labels, values, len(labels)]


def format_data(data):
    data['aveFriendCount']      = int(round(data['aveFriendCount']))
    data['aveRetweetCount']     = int(round(data['aveRetweetCount']))
    data['avReplyCount']        = int(round(100*data['avReplyCount']))/100
    data['aveHashtagsInTweets'] = int(round(100*data['aveHashtagsInTweets']))/100
    data['percentagePosTweets'] = int(round(100*data['percentagePosTweets']))/100
    data['percentageNegTweets'] = int(round(100*data['percentageNegTweets']))/100
    data['percentageNegTweets'] = int(round(data['percentageNegTweets']*100))/100
    data['percentagePosTweets'] = int(round(data['percentagePosTweets']*100))/100
    return data
