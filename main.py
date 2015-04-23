from load_data import load_data
import sentiment
import sys


def main():
    tweet_df = load_data(1000)
    company_names = ['intel', 'ibm', 'goldman']
    sentiment_types = ['linear', 'sigmoid', 'logistic']
    for company in company_names:
        tweets = sentiment.get_company_tweets(tweet_df, company)
        sentiment_predictions = sentiment.analysis(tweets, sentiment_types[0])
        tweet_df = sentiment.add_to_dataframe(tweet_df, company, sentiment_predictions)


if __name__ == '__main__':
    main()