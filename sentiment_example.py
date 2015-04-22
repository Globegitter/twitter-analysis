"""Build a sentiment analysis / polarity model
Sentiment analysis can be casted as a binary text classification problem,
that is fitting a linear classifier on features extracted from the text
of the user messages so as to guess wether the opinion of the author is
positive or negative.
In this examples we will use a movie review dataset.
"""
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
import random
from sklearn import metrics
from load_data import load_data
from pandas import Series
from sklearn import svm
from sklearn.linear_model import LogisticRegression



if __name__ == "__main__":
    # NOTE: we put the following in a 'if __name__ == "__main__"' protected
    # block to be able to use a multi-core grid search that also works under
    # Windows, see: http://docs.python.org/library/multiprocessing.html#windows
    # The multiprocessing module is used as the backend of joblib.Parallel
    # that is used when n_jobs != 1 in GridSearchCV

    # the training data folder must be passed as first argument
    # movie_reviews_data_folder = 'movie_example_data'
    # dataset = load_files(movie_reviews_data_folder, shuffle=False)
    # print("n_samples: %d" % len(dataset.data))

    # split the dataset in training and test set:
    # docs_train, docs_test, y_train, y_test = train_test_split(
    #     dataset.data, dataset.target, test_size=0.25, random_state=None)

    # print('docs_train', docs_train)
    # sys.exit(0)

    tweets_df = load_data(100)
    intel_tweets = tweets_df[tweets_df['Symbol'] == 'intel']['Text'].values
    y = [round(random.uniform(0.1, 1.0), 10) for i in intel_tweets]


    clf = svm.SVC(kernel='linear')
    clf2 = svm.SVC(kernel='sigmoid')
    logreg = LogisticRegression(C=1000)
    # TASK: Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
        ('clf', LinearSVC(C=1000)),
    ])

    # TASK: Build a grid search to find out whether unigrams or bigrams are
    # more useful.
    # Fit the pipeline on the training set using grid search for the parameters
    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
    }
    # You can set the parameters using the names issued
    #  For instance, fit using a k of 10 in the SelectKBest
    #  and a parameter 'C' of the svm
    fit_val = pipeline.set_params(vect__ngram_range=(1, 2)).fit(intel_tweets, y)
    print('fit_val', fit_val)
    prediction = pipeline.predict(intel_tweets)

    # tweets_df[tweets_df['Symbol'] == 'intel']['text_prediction'] =
    # Series(prediction, index=tweets_df[tweets_df['Symbol'] == 'intel'].index)

    # for df in tweets_df[tweets_df['Symbol'] == 'intel']:
    #     print(df)
    #     df['text_sentiment'] = prediction

    intel_df = tweets_df[tweets_df['Symbol'] == 'intel']
    intel_df['Sentiment_Score'] = prediction
    print(intel_df)
    # print('prediction', prediction.shape)
    # print('len2', tweets_df[tweets_df['Symbol'] == 'intel']['Text'].values.shape)
    # grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
    # grid_search.fit(docs_train, y_train)

    # TASK: print the cross-validated scores for the each parameters set
    # explored by the grid search
    # print(grid_search.grid_scores_)

    # TASK: Predict the outcome on the testing set and store it in a variable
    # named y_predicted
    # y_predicted = grid_search.predict(docs_test)

    # Print the classification report
    # print(metrics.classification_report(y_test, y_predicted,
    #                                     target_names=dataset.target_names))

    # Print and plot the confusion matrix
    # cm = metrics.confusion_matrix(y_test, y_predicted)
    # print(cm)

    # import matplotlib.pyplot as plt
    # plt.matshow(cm)
    # plt.show()