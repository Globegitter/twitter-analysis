from load_data import load_data
import sentiment
import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
import datetime as dt
import statistics


def regression_agent(sentiment_data, prices_data, symbol):
    sentiment_df = sentiment_data[sentiment_data['Symbol'] == symbol]

    start_date = min(sentiment_df['Date']).date()
    end_date = max(sentiment_df['Date']).date()

    sentiment_df = sentiment_df[['Date', 'Weighted_Sentiment_Score']]

    sentiment_df = aggregate_to_daily_summaries(sentiment_df)

    prices_data = prices_data.iloc[::-1]

    prices_df = prices_data[symbol]
    prices_df = prices_data[prices_data['Date'] >= start_date]
    prices_df = prices_df[prices_data['Date'] <= end_date].set_index('Date')

    reg_data = prices_df.join(sentiment_df)

    y = reg_data[symbol]
    X = reg_data[['Weighted_Sentiment_Score']]
    X['ones'] = np.ones((len(sentiment_df), ))
    result_object = sm.OLS(y, X).fit()
    return result_object


def aggregate_to_daily_summaries(sentiment_data):
    sentiment_data['just_date'] = [x.date() for x in sentiment_data['Date']]
    return sentiment_data.groupby('just_date').aggregate(np.mean)


@profile
def main():
    tweet_df = load_data(100000)
    # sys.exit(0)
    company_names = ['intel', 'ibm', 'goldman']
    sentiment_types = ['linear', 'sigmoid', 'logistic']

    print("Data load completed.")

    for company in ['intel']:  # company_names
        tweets = sentiment.get_company_tweets(tweet_df, company)

        # sentiment_predictions = sentiment.analysis_multi(tweets, sentiment_types[0])
        sentiment_predictions = sentiment.analysis(tweets, sentiment_types[0])
        # print('sentiment_predictions multi', sentiment_predictions)
        # print('length', len(sentiment_predictions))
        # print('mean', statistics.mean(sentiment_predictions))
        # print('median', statistics.median(sentiment_predictions))

        # sentiment_predictions2 = sentiment.analysis(tweets, sentiment_types[0])
        # print('sentiment_predictions', sentiment_predictions2)
        # print('length', len(sentiment_predictions2))
        # print('mean', statistics.mean(sentiment_predictions2))
        # print('median', statistics.median(sentiment_predictions2))
        tweet_df = sentiment.add_to_dataframe(tweet_df, company, sentiment_predictions)

    print("Sentiment Analysis completed.")

    prices_df_original = pd.read_csv('prices_data.csv')
    prices_df_original['Date'] = [dt.datetime.strptime(x, '%d/%m/%Y') for x in prices_df_original['Date']]

    tweet_df['Weighted_Sentiment_Score'] = tweet_df['Sentiment_Score'] * tweet_df['Followers']

    intel_regressor = regression_agent(tweet_df, prices_df_original, 'intel')

    print(intel_regressor.summary())


if __name__ == '__main__':
    main()