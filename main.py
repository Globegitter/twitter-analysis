from load_data import load_data
import sentiment
import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
import datetime as dt
from graphs import plot_data


def regression_agent(sentiment_data, prices_data, symbol):
    sentiment_df = sentiment_data[sentiment_data['Symbol'] == symbol]

    start_date = min(sentiment_df['Date']).date()
    end_date = max(sentiment_df['Date']).date()

    sentiment_df = sentiment_df[['Date', 'Weighted_Sentiment_Score']]

    sentiment_df, unique_dates = aggregate_to_daily_summaries(sentiment_df)

    prices_data = prices_data.iloc[::-1]

    # print('start date of read data', start_date)
    # print('end date of read data', end_date)

    # prices_df = prices_data[symbol]
    prices_df = prices_data[prices_data['Date'] >= start_date]
    # print(prices_df)
    prices_df = prices_df[prices_data['Date'] <= end_date].set_index('Date')
    # print(prices_df)

    reg_data = prices_df.join(sentiment_df)
    # print(reg_data)
    # print(len(sentiment_df))

    y = reg_data[symbol]
    X = reg_data[['Weighted_Sentiment_Score']]
    X['ones'] = np.ones((len(reg_data), ))
    if len(reg_data) != len(sentiment_df):
        print('Waring! Data about some days was missing so these days have been deleted.')
        print('Number of days in the prediction data set', len(sentiment_df))
        print('Number of days in the dow jones data set', len(reg_data))
    result_object = sm.OLS(y, X).fit()
    return result_object, unique_dates


def unique(seq):
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


def aggregate_to_daily_summaries(sentiment_data):
    dates = [x.date() for x in sentiment_data['Date']]
    sentiment_data['just_date'] = dates
    return sentiment_data.groupby('just_date').aggregate(np.mean), unique(dates)


# @profile
def main():
    print('Loading data now...')
    tweet_df = load_data(200000)
    # sys.exit(0)
    company_names = ['intel', 'ibm', 'goldman']
    sentiment_types = ['linear', 'sigmoid', 'logistic']

    print("Data load completed.")

    for company in ['intel']:  # company_names
        tweets = sentiment.get_company_tweets(tweet_df, company)

        sentiment_predictions = sentiment.analysis_multi(tweets, sentiment_types[0])
        print('number of tweets for intel', len(sentiment_predictions))
        # sentiment_predictions = sentiment.analysis(tweets, sentiment_types[0])

        tweet_df = sentiment.add_to_dataframe(tweet_df, company, sentiment_predictions)

    print("Sentiment Analysis completed.")

    prices_df_original = pd.read_csv('prices_data.csv')
    dow_jone_dates = [dt.datetime.strptime(x, '%d/%m/%Y') for x in prices_df_original['Date']]
    prices_df_original['Date'] = dow_jone_dates
    print(prices_df_original)
    # print('last two', prices_df_original)
    # print('last two', prices_df_original['intel'].values.tolist()[-2:])
    # print(dow_jone_dates[-2:])

    tweet_df['Weighted_Sentiment_Score'] = tweet_df['Sentiment_Score'] * tweet_df['Followers']

    intel_regressor, dates = regression_agent(tweet_df, prices_df_original, 'intel')
    prediction = intel_regressor.predict()
    print(prediction)

    prediction_data = list(zip(dates, prediction))
    dow_jone_dates = dow_jone_dates[-len(dates):]
    dow_jone_dates = dow_jone_dates[::-1]
    intel_prices = prices_df_original['intel'].values.tolist()[-len(dates):]
    intel_prices = intel_prices[::-1]

    dow_jones_data = list(zip(dow_jone_dates, intel_prices))

    plot_data(prediction_data, dow_jones_data)


if __name__ == '__main__':
    main()