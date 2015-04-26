from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import datetime as dt

# accepts pairs of prediction data, dow_jones data
def plot_data(labels, *data_pairs):

    if len(data_pairs) % 2 != 0 or len(data_pairs) > 6:
        raise LookupError('Graphing only supports plotting of data in pairs and up to 6 in total.')

    # prediction_data = [(dt.datetime.strptime('2010-02-05', "%Y-%m-%d"), 123),
    #     (dt.datetime.strptime('2010-02-19', "%Y-%m-%d"), 678),
    #     (dt.datetime.strptime('2010-03-05', "%Y-%m-%d"), 987),
    #     (dt.datetime.strptime('2010-03-19', "%Y-%m-%d"), 345)]
    # print(prediction_data)

    # data2 = [(dt.datetime.strptime('2010-02-05', "%Y-%m-%d"), 500),
    #     (dt.datetime.strptime('2010-02-19', "%Y-%m-%d"), 300),
    #     (dt.datetime.strptime('2010-03-05', "%Y-%m-%d"), 400),
    #     (dt.datetime.strptime('2010-03-19', "%Y-%m-%d"), 200)]

    args = []
    colors = ['r-o', 'b-o', 'g-o', 'c-o', 'm-o', 'y-o']

    for i in range(0, len(data_pairs), 2):
        x = [date2num(date) for (date, value) in data_pairs[i]]
        y = [value for (date, value) in data_pairs[i]]

        x2 = [date2num(date) for (date, value) in data_pairs[i + 1]]
        y2 = [value for (date, value) in data_pairs[i + 1]]

        args.extend([x, y, colors[i], x2, y2, colors[i + 1]])

    args = tuple(args)

    fig = plt.figure(1)

    graph = fig.add_subplot(111)

    # Plot the data as a red line with round markers
    graph.plot(*args)

    # Set the xtick locations to correspond to just the dates you entered.
    # graph.set_xticks(x)

    # Set the xtick labels to correspond to just the dates you entered.
    # graph.set_xticklabels(
    #     [date.strftime("%Y-%m-%d") for (date, value) in data_pairs[0]]
    #     )
    graph.legend(labels)
    plt.show()


if __name__ == '__main__':
    plot_data()