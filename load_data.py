import numpy as np
import pandas as pd
import json
import sys


def load_data():
    # file_path = '../exampletweets_2.txt'
    file_path = 'format_example.txt'
    if len(sys.argv) > 2:
        file_path = sys.argv[2]

    max_json_objects = 10
    nr_json_objects = 0
    nr_open_brackets = 0
    # nr_close_brackets = 0
    chars_read = ''
    tweets = pd.DataFrame()

    with open(file_path, "r", encoding="utf-8") as file:
        while nr_json_objects < max_json_objects:
            c = file.read(1)
            if not c:
                break
            if c == '{':
                nr_open_brackets += 1
            if c == '}':
                nr_open_brackets -= 1

            chars_read += c

            if nr_open_brackets == 0:
                nr_json_objects += 1

                print(chars_read)
                tweet = pd.read_json(chars_read)
                chars_read = ''

                if tweets.empty:
                    tweets = tweet
                else:
                    pd.concat([tweets, tweet])

        print('nr of json objects', nr_json_objects)
        print(tweets)

    # data = json.load(f)
    # data = pandas.read_json('single_json.txt')
    # print(data)