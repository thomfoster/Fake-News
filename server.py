import helpers
import fake_news_checker
from flask import Flask, render_template, url_for, request, redirect, jsonify
import twython
app = Flask(__name__)

APP_KEY, ACCESS_TOKEN = helpers.get_credentials()
twitter = twython.Twython(APP_KEY, access_token=ACCESS_TOKEN)

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
    data = fake_news_checker.check(search_string, twitter)
    return render_template('resultsTEMPLATE.html',
                            search_string=helpers.readable_from_url(search_string),
                            data=data)
