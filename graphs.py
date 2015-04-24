from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import datetime as dt


def plot_data(prediction_data, dow_jones_data):
    # prediction_data = [(dt.datetime.strptime('2010-02-05', "%Y-%m-%d"), 123),
    #     (dt.datetime.strptime('2010-02-19', "%Y-%m-%d"), 678),
    #     (dt.datetime.strptime('2010-03-05', "%Y-%m-%d"), 987),
    #     (dt.datetime.strptime('2010-03-19', "%Y-%m-%d"), 345)]
    # print(prediction_data)

    # data2 = [(dt.datetime.strptime('2010-02-05', "%Y-%m-%d"), 500),
    #     (dt.datetime.strptime('2010-02-19', "%Y-%m-%d"), 300),
    #     (dt.datetime.strptime('2010-03-05', "%Y-%m-%d"), 400),
    #     (dt.datetime.strptime('2010-03-19', "%Y-%m-%d"), 200)]

    x = [date2num(date) for (date, value) in prediction_data]
    y = [value for (date, value) in prediction_data]

    x2 = [date2num(date) for (date, value) in dow_jones_data]
    y2 = [value for (date, value) in dow_jones_data]

    fig = plt.figure(1)

    graph = fig.add_subplot(111)

    # Plot the data as a red line with round markers
    graph.plot(x, y, 'r-o', x2, y2, 'b-o')

    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x)

    # Set the xtick labels to correspond to just the dates you entered.
    graph.set_xticklabels(
        [date.strftime("%Y-%m-%d") for (date, value) in prediction_data]
        )
    graph.legend(['Prediction', 'Dow Jones'])
    plt.show()


if __name__ == '__main__':
    plot_data()