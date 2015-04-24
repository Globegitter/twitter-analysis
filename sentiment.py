"""Builds a sentiment analysis / polarity model
Sentiment analysis can be casted as a binary text classification problem,
that is fitting a classifier on features extracted from the text
of the user messages so as to guess wether the opinion of the author is
positive or negative.
"""
# Based on the work by Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import random
from sklearn import svm
from sklearn.linear_model import LogisticRegression
import numpy as np
from joblib import Parallel, delayed


# @profile
def analysis(tweets, method='linear'):

    classification = svm.SVC(kernel='linear')

    if method == 'sigmoid':
        classification = svm.SVC(kernel='sigmoid')
    elif method == 'logistic':
        classification = LogisticRegression(C=1000)

    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
        ('classification', classification),
    ])

    y = [round(random.uniform(0.0, 1.0)) for tweet in tweets]

    pipeline.set_params(vect__ngram_range=(1, 2))
    pipeline.fit(tweets, y)
    sentiment_predictions = pipeline.predict(tweets)

    return sentiment_predictions


def chunks(l, number):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), number):
        yield l[i:i + number]


def get_company_tweets(df, name):
    return df[df['Symbol'] == name]['Text'].values


def add_to_dataframe(df, name, sentiment_predictions):

    # make sure the data frame has the right column

    if 'Sentiment_Score' not in df.columns:
        df['Sentiment_Score'] = np.random.randn(df.shape[0])

    symbol_df = df[df['Symbol'] == name]
    symbol_df['Sentiment_Score'] = sentiment_predictions

    # add the sentiment predictions to the original sentiment_prediction
    df[df['Symbol'] == name] = symbol_df

    return df
