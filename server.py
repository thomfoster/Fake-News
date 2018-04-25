import helpers
import fake_news_checker
from flask import Flask, render_template, url_for, request, redirect, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('searchTEMPLATE.html')

@app.route('/', methods=['POST'])
def search():
    search_string = request.form['data']
    search_string = helpers.url_from_form(search_string) #delimit by "-" etc
    return redirect(url_for('results', search_string=search_string))

@app.route('/results/<search_string>')
def results(search_string):
    data = fake_news_checker.check(search_string.replace('-', ' '))
    if data['nTweets'] < 100:
        return redirect(url_for('fail', search_string=search_string))
    time_chart_data = helpers.format_for_time_chart(data)
    labels = ["Positive Tweets", "Neutral Tweets", "Negative Tweets"]
    values = [data['percentagePosTweets']*100, 100 - data['percentagePosTweets']*100 - data['percentageNegTweets']*100, data['percentageNegTweets']*100]
    colors = [ "#28A745",  "#5bc0de" , "#d9534f"]
    data['aveFriendCount'] = int(round(data['aveFriendCount']))
    data['aveRetweetCount'] = int(round(data['aveRetweetCount']))
    data['avReplyCount'] = int(round(data['avReplyCount']))
    data['aveHashtagsInTweets'] = int(round(data['aveHashtagsInTweets']))
    data['percentagePosTweets'] = int(round(100*data['percentagePosTweets']))/100
    data['percentageNegTweets'] = int(round(100*data['percentageNegTweets']))/100
    return render_template('resultsTEMPLATE.html',
                            search_string=helpers.readable_from_url(search_string),
                            data=data,
                            time_chart_data=time_chart_data,
                            set=zip(values, labels, colors))

@app.route('/fail/<search_string>')
def fail(search_string):
    return render_template('failTEMPLATE.html',
                            search_string=helpers.readable_from_url(search_string))
