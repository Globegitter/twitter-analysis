import numpy as np
import pandas as pd
import json as js
import sys


def load_data():
    #file_path = '../exampletweets_2.txt'
    file_path = 'format_example.txt'
    if len(sys.argv) > 2:
        file_path = sys.argv[2]

    max_json_objects = 10
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

                print(chars_read)
                tweet = js.loads(chars_read)
                chars_read = ''

                if len(tweet) > 0:
                    tweets.append(tweet)

        print('nr of json objects', nr_json_objects)

        keywords_list = ['Intel', 'intel', 'IBM', 'ibm', 'Goldman', 'goldman', '$INTC', '$GS', '$IBM', '$intc', '$gs', '$ibm']
        stock_to_keyword_mapper = {'Intel': 'intel', 'intel': 'intel', 'IBM': 'ibm', 'ibm': 'ibm', 'Goldman': 'goldman', 'goldman': 'goldman', '$INTC' :'intel', '$GS': 'goldman', '$IBM': 'ibm', '$intc': 'intel', '$gs': 'goldman', '$ibm': 'ibm'}

        tweets_list = []

        for tweet in tweets:
            tweets_list.append(assign_stock_to_tweet(tweet, keywords_list, stock_to_keyword_mapper))

        df = pd.DataFrame(tweets_list, columns=['Symbol', 'Text', 'Retweet_Count', 'Favorite_Count'])

        print(df)

    # data = json.load(f)
    # data = pandas.read_json('single_json.txt')
    # print(data)

def assign_stock_to_tweet(tweet, keywords_list, stock_to_keyword_mapper):
    for keyword in keywords_list:
        if keyword in tweet['text']:
            return (stock_to_keyword_mapper[keyword], tweet['text'], tweet['retweet_count'], tweet['favorite_count'])