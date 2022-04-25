import json
import pandas as pd
from textblob import TextBlob
import zipfile


def read_json(json_file: str) -> list:
    tweets_data = []
    with zipfile.ZipFile("json_file", "r") as z:
        for tweets in z.open(json_file, 'r'):
            tweets_data.append(json.loads(tweets.decode("utf-8")))
        return len(tweets_data), tweets_data


class TweetDfExtractor:

    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    def find_statuses_count(self) -> list:
        statuses_count = []
        for tweet in self.tweets_list:
            statuses_count.append(tweet['user']['statuses_count'])
        return statuses_count

    def find_full_text(self) -> list:
        text = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys() and 'text' in tweet['retweeted_status'].keys():
                text.append(tweet['retweeted_status']['text'])
            else:
                text.append('Empty')
        return text

    def find_sentiments(self, text: list) -> list:
        polarity = []
        subjectivity = []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return polarity, subjectivity

    def find_created_time(self) -> list:
        created_at = []
        for time in self.tweets_list:
            created_at.append(time['created_at'])
        return created_at
