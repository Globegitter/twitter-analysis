import numpy as np
import pandas as pd
import json as js
import sys
from sklearn.preprocessing import StandardScaler


def load_data(max_json_objects=10):
    file_path = '../exampletweets_2.txt'
    # file_path = 'format_example.txt'
    if len(sys.argv) > 2:
        file_path = sys.argv[2]

    nr_json_objects = 0
    nr_open_brackets = 0
    # nr_close_brackets = 0
    chars_read = ''
    tweets = []

    with open(file_path, "r", encoding="utf-8") as file:
        while nr_json_objects < max_json_objects:
            c = file.read(1)
            if not c:
                break
            if c == '{':
                nr_open_brackets += 1
            if c == '}':
                nr_open_brackets -= 1

            chars_read += c

            if nr_open_brackets == 0:
                nr_json_objects += 1

                tweet = js.loads(chars_read)
                chars_read = ''

                tweets.append(tweet)

        keywords_list = ['Intel', 'intel', 'IBM', 'ibm', 'Goldman', 'goldman', '$INTC', '$GS', '$IBM', '$intc', '$gs', '$ibm']
        stock_to_keyword_mapper = {'Intel': 'intel', 'intel': 'intel', 'IBM': 'ibm', 'ibm': 'ibm', 'Goldman': 'goldman', 'goldman': 'goldman', '$INTC' :'intel', '$GS': 'goldman', '$IBM': 'ibm', '$intc': 'intel', '$gs': 'goldman', '$ibm': 'ibm'}

        tweets_list = []

        for tweet in tweets:
            tweets_list.append(assign_stock_to_tweet(tweet, keywords_list, stock_to_keyword_mapper))

        tweets_list = [tweet for tweet in tweets_list if tweet is not None]
        df = pd.DataFrame(tweets_list, columns=['Date', 'Symbol', 'Text', 'Followers'])

        scaler = StandardScaler()
        for column in ['Followers']:
            df[column] = scaler.fit(df[column]).transform(df[column])

        # print(df)

    # intel_tweets = df[df['Symbol'] == 'intel']['Text'].values
    # print(intel_tweets)

    return df

    # data = json.load(f)
    # data = pandas.read_json('single_json.txt')
    # print(data)


def assign_stock_to_tweet(tweet, keywords_list, stock_to_keyword_mapper):
    for keyword in keywords_list:
        if keyword in tweet['text']:
            return (pd.to_datetime(tweet['created_at']), stock_to_keyword_mapper[keyword], tweet['text'], tweet['user']['followers_count'])

