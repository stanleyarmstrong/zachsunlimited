import pandas as pd
import json
import requests
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os
from flask import Flask, render_template
stopwords = set(stopwords.words("english"))
stemmer = PorterStemmer()
from watson_developer_cloud import AuthorizationV1 as WatsonAuthorization
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
alchemy = AlchemyLanguage(api_key=os.environ.get("ALCHEMY_API_KEY"))


def URL_builder(api_key, begin_date, end_date, page=0):
    '''
    INPUT: NYT API key, begin date (YYYYMMDD), end date, page
    OUTPUT: URL with JSON information about given day's headlines
    '''
    URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?{}={}&{}={}&{}={}&{}={}&fq=news_desk:("World")'.\
        format('api-key', api_key, 'begin-date', begin_date, 'end-date', end_date, 'page', page)
    return URL

def get_week_strings(seed):
    '''
    OUTPUT: Takes int and outputs list of previous 7 integers
    '''
    return [str(i+1) for i in range(seed-7, seed)]

def create_headline_df(date_list):
    '''
    INPUT: date in format 'YYYYMMDD' (Calling multiple dates can time out API)
    OUTPUT: Pandas dataframe with columns for headlines and associated date
    '''
    api_key = 'aa955d9919794bb9a66785e7c52c3cb5'
    data_tuples = []
    for date in date_list:
        print(date)
        re = requests.get(URL_builder(api_key, date, date), timeout = 1000)
        json_dict = json.loads(re.text)

    #         JSON Dictionaries are pretty icky ... we'll crawl through them and find what we need
        for item in json_dict['response']['docs']:
            if 'main' in item['headline'].keys():
    #           data_tuples.append((item['pub_date'], item['headline']['main']))
                data_tuples.append((date, item['headline']['main']))

    labels = ['Date', 'Headline']
    return pd.DataFrame.from_records(data_tuples, columns=labels)

def word_cleaning(df):
    '''
    OUTPUT: Dataframe, grouped by date, Headline is stemmed headline words
    '''
    data_tuples = []
    # Look at each date, clean strings, remove stopwords, etc.
    for row in df.groupby('Date').agg(lambda x : ' '.join(x)).iterrows():
        words = row[1]['Headline']
        #Clean darta
        letters_only = re.sub("[^\sa-zA-Z]", "", words)
        tokenized_words = [word for word in letters_only.lower().split() if not word in stopwords]
        word_cloud = ' '.join(tokenized_words)
        data_tuples.append((row[0], word_cloud))
    labels = ['Date', 'headline_words']

    #Return results as pandas dataframe
    return pd.DataFrame.from_records(data_tuples, columns=labels)

def get_sentiment(df):
    '''
    INPUT: Pandas dataframe with date and words
    OUTPUT: Score of how terrible the day was
    '''
    row_avg_scores = []
    for row in df.iterrows():
        score = 0
        for word in row[1]['headline_words'].split():
            print(word)
            print('-')
            result = alchemy.sentiment(word)
            try:
                val = float(result['docSentiment']['score'])
            except KeyError: #neutral words
                val = 0
            score += val
        row_avg_scores.append((row[1]['Date'], score/len(row[1]['headline_words'])))
    labels = ['Date', 'avg_score']
    return pd.DataFrame.from_records(row_avg_scores, columns=labels)

def day_ranker(num):
    '''
    INPUT: A day's average word sentiment
    OUTPUT: scale of 1 to 10 of how bad the day is
    '''
    if num > 0:
        return 1
    else:
        return 10

def get_value_and_words(date):
    '''
    INPUT: Date ('YYYYMMDD')
    OUTPUT: Ranking of how terrible day is from 1-10, list of words from API
    '''
    df1 = create_headline_df([date])
    df2 = word_cleaning(df1)
    df3 = get_sentiment(df2)
    day_ranking = day_ranker(df3.ix[0,'avg_score'])
    return day_ranking, df2.ix[0,'headline_words'].split()

app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def index():
    # day_rank, words = get_value_and_words('20070130')
    day_rank = 10
    # return app.send_static_file("index.html")
    return render_template('index.html', result = day_rank)
    # return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)
