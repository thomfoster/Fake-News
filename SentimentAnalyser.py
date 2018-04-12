import nltk, json, csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

################################################################################################

# main analyse csv function
def analyseCSV(csvDir):
    # open file and take first line
    file = open(csvDir, newline='')
    reader = csv.reader(file)

    # list of dictionaries for each topic, containing average scores
    # compound - overall impression
    # neg - negative level
    # neu - neutral level
    # pos - positive level
    output = []

    # analyse each topic
    for topic in reader:
        name = topic[0]
        output.append([name, analyseTopic(topic)])
        print(name + " analysed.")

    return output


# topic anlysis function - input: csv line, output: average scores dictionary 
def analyseTopic(topic):
    averageScores = {"compound": 0.0, "neg": 0.0, "neu": 0.0, "pos": 0.0, "compound_var": 0.0} # average scores dict
    formattedTweets = formatInput(topic)

    # analyse each individual tweet
    for tweet in formattedTweets:
        # load JSON object and extract text value
        tweetDict = json.loads(tweet)
        text = tweetDict["text"]
        
        scores = analyseText(text)
        for k in ["compound", "neg","neu", "pos"]: # add to score averages
            averageScores[k] = averageScores[k] + scores[k]
        averageScores["compound_var"] = averageScores["compound_var"] + scores["compound"]*scores["compound"] 

    # take average
    for k in ["compound", "neg","neu", "pos"]:
        averageScores[k] = round(averageScores[k]/(len(formattedTweets)), 4)
    averageScores["compound_var"] = averageScores["compound_var"]/(len(formattedTweets)) - averageScores["compound"]*averageScores["compound"]

    # dump to JSON
    jsonScores = json.dumps(averageScores)
    return jsonScores


# text analysis function - input: text string, output: sentiment scores
def analyseText(text):
    # instantiate sentiment analyser object NLTK
    analyzer = SentimentIntensityAnalyzer()

    # create list of scores of sentiment - compound gives overall impression (-1 most negative, 1 most positive)
    scores = analyzer.polarity_scores(text)
    return scores


# format csv line list into useable tweet list
def formatInput(tweets):
    formattedTweets = [x for x in tweets if x != "{}"] # remove empty JSON objects
    formattedTweets.pop(0) # remove name of topc

    return formattedTweets


################################################################################################

# create output CSV for tweetX inputs

files = ["tweets0.csv", "tweets1.csv", "tweets2.csv", "tweets3.csv", "tweets4.csv", "tweets5.csv",
         "tweets6.csv", "tweets7.csv", "tweets8.csv", "tweets9.csv"]

# main loop, analyse each file in turn
with open("semanticResults.csv", "w", newline = '') as outputFile:
    writer = csv.writer(outputFile)
    for fileName in files:
        analysis = analyseCSV(fileName)
        writer.writerows(analysis)


        
    

