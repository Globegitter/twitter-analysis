import numpy as np
import pandas as pd
import json as js
import sys
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as sm
import timeit


def load_data(max_json_objects=10):
    file_path = '../exampletweets_2.txt'
    # file_path = 'format_example.txt'
    if len(sys.argv) > 2:
        file_path = sys.argv[2]

    nr_json_objects = 0
    chars_read = ''
    tweets = []

    with open(file_path, "r", encoding="ISO-8859-1") as file:

        while nr_json_objects < max_json_objects:
            c = file.read(10000)
            if not c:
                break

            chars_read += c
            json_end = chars_read.find('}{')

            while json_end > -1:
                nr_json_objects += 1

                chars_read_tw1 = chars_read[0:json_end + 1]

                tweet = js.loads(chars_read_tw1)
                tweets.append(tweet)

                chars_read = chars_read[chars_read.find('}{') + 1:]
                json_end = chars_read.find('}{')

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

    prices_df_original = pd.read_csv('prices_data.csv').set_index('Date')

    intel_regressor = regression_agent(df, prices_df_original, 'intel')

    print(intel_regressor.summary())

    # data = json.load(f)
    # data = pandas.read_json('single_json.txt')
    # print(data)


def assign_stock_to_tweet(tweet, keywords_list, stock_to_keyword_mapper):
    for keyword in keywords_list:
        if keyword in tweet['text']:
            return (pd.to_datetime(tweet['created_at']), stock_to_keyword_mapper[keyword], tweet['text'], tweet['user']['followers_count'])


def regression_agent(sentiment_data, prices_data, symbol):
    sentiment_df = sentiment_data[sentiment_data['Symbol'] == symbol]

    sentiment_df = aggregate_to_daily_summaries(sentiment_df)

    start_date = min(sentiment_df['Date'])
    end_date = max(sentiment_df['Date'])

    prices_df = prices_data[start_date:end_date]

    y = prices_df[symbol]
    X = sentiment_df[['Followers', 'Sentiment_Score']]
    X['ones'] = np.ones((len(sentiment_df), ))
    result_object = sm.OLS(y, X).fit()
    return result_object


def aggregate_to_daily_summaries(sentiment_data):
    return sentiment_data.groupby('Date').aggregate(np.mean)
