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
    # print(unique_dates)

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
    tweet_df = load_data(10000000)
    company_names = ['intel', 'ibm', 'goldman']
    sentiment_types = ['linear', 'sigmoid', 'logistic']
    plot_labels = []
    plot_args = []

    print("Data load completed. Number of tweets in total: " + str(len(tweet_df)))

    prices_df_original = pd.read_csv('prices_data.csv')
    dow_jone_dates = [dt.datetime.strptime(x, '%d/%m/%Y') for x in prices_df_original['Date']]
    dow_jone_dates = dow_jone_dates[::-1]
    prices_df_original['Date'] = dow_jone_dates

    for company in company_names:
        print(tweet_df[tweet_df['Symbol'] == company].values)
        tweets = sentiment.get_company_tweets(tweet_df, company)
        print("Number of Tweets for " + company + ": " + str(len(tweets)))

        sentiment_predictions = sentiment.analysis_multi(tweets, sentiment_types[2])
        # sentiment_predictions = sentiment.analysis(tweets, sentiment_types[0])

        tweet_df = sentiment.add_to_dataframe(tweet_df, company, sentiment_predictions)

        print("Sentiment Analysis completed for " + company + ".")

        tweet_df['Weighted_Sentiment_Score'] = tweet_df['Sentiment_Score'] * tweet_df['Followers']

        company_regressor, dates = regression_agent(tweet_df, prices_df_original, company)
        prediction = company_regressor.predict()

        prediction_data = list(zip(dates, prediction))
        # print(dow_jone_dates)
        dow_jone_dates_company = dates
        company_prices = prices_df_original[company].values.tolist()[-len(dates):]
        company_prices = company_prices[::-1]

        dow_jones_data = list(zip(dow_jone_dates_company, company_prices))

        plot_labels.extend([company + ' P', company + ' DJ'])
        plot_args.extend([prediction_data, dow_jones_data])
        print("Predictions completed and stored for " + company + ".")

    # print(plot_args)

    plot_data(plot_labels, *tuple(plot_args))


if __name__ == '__main__':
    main()