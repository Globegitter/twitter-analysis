import pandas as pd
import ujson
import sys
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed
from memoized import memoized


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
            c = file.read(100000)
            if not c:
                break

            chars_read += c
            json_end = chars_read.find('}{')

            while json_end > -1:
                nr_json_objects += 1

                chars_read_tw1 = chars_read[0:json_end + 1]
                # print(chars_read_tw1)
                tweet = ujson.loads(chars_read_tw1)
                tweets.append(tweet)

                chars_read = chars_read[json_end + 1:]
                json_end = chars_read.find('}{')

        keywords_list = ['Intel', 'intel', 'IBM', 'ibm', 'Goldman', 'goldman', '$INTC', '$GS', '$IBM', '$intc', '$gs', '$ibm']
        stock_to_keyword_mapper = {'Intel': 'intel', 'intel': 'intel', 'IBM': 'ibm', 'ibm': 'ibm', 'Goldman': 'goldman', 'goldman': 'goldman', '$INTC' :'intel', '$GS': 'goldman', '$IBM': 'ibm', '$intc': 'intel', '$gs': 'goldman', '$ibm': 'ibm'}

        tweets_list = Parallel(n_jobs=4, backend="threading")(delayed(assign_stock_to_tweet)(tweet, keywords_list, stock_to_keyword_mapper) for tweet in tweets)

        # tweets_list = []
        #
        # for tweet in tweets:
        #     tweets_list.append(assign_stock_to_tweet(tweet, keywords_list, stock_to_keyword_mapper))

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
            # first = pd.to_datetime(tweet['created_at'])
            first = to_timestamp(tweet['created_at'])
            # first = pd.Timestamp(tweet['created_at'])
            second = stock_to_keyword_mapper[keyword]
            third = tweet['text']
            fourth = tweet['user']['followers_count']
            return first, second, third, fourth


@memoized
def to_timestamp(date_time):
    return pd.Timestamp(date_time)
