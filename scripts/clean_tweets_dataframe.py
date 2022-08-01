import pandas as pd
from bs4 import BeautifulSoup
import re
import sys
import os
from nltk.corpus import stopwords

sys.path.append(os.path.abspath(os.path.join('data')))


class CleanTweets:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        print('Cleaning in progress...')

    def drop_unwanted_column(self) -> pd.DataFrame:
        columns = ['created_at', 'source', 'original_text', 'retweet_text', 'sentiment', 'polarity',
                   'subjectivity', 'lang', 'statuses_count', 'favorite_count', 'retweet_count',
                   'screen_name', 'followers_count', 'friends_count', 'possibly_sensitive',
                   'hashtags', 'user_mentions', 'location']
        unwanted_rows = []
        for columnName in columns:
            unwanted_rows = self.df[self.df[columnName] == columnName].index
            self.df.drop(unwanted_rows, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
        return self.df

    def drop_nullValue(self) -> pd.DataFrame:
        self.df.dropna(subset=['original_text', 'retweet_text'], inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def drop_duplicate(self) -> pd.DataFrame:
        self.df.drop_duplicates(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def convert_to_datetime(self) -> pd.DataFrame:
        self.df['created_at'] = pd.to_datetime(
            self.df['created_at'], errors='coerce')
        return self.df

    def convert_to_numbers(self) -> pd.DataFrame:
        self.df[['sentiment', 'polarity', 'subjectivity', 'statuses_count', 'favorite_count', 'retweet_count',
                 'followers_count', 'friends_count']] = self.df[['sentiment', 'polarity', 'subjectivity', 'statuses_count', 'favorite_count', 'retweet_count',
                                                                 'followers_count', 'friends_count']].apply(pd.to_numeric, errors='coerce')
        return self.df

    def remove_non_english_tweets(self) -> pd.DataFrame:
        index_names = self.df[self.df['lang'] != 'en'].index
        self.df.drop(index_names, inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def remove_emoji(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def clean_retweet_text(self) -> pd.DataFrame:
        self.df['retweet_text'] = self.df['retweet_text'].apply(
            lambda x: " ".join(x.lower() for x in x.split()))  # lowercase
        self.df['retweet_text'] = self.df['retweet_text'].str.replace(
            '[^\w\s]', '')  # remove punctuation
        self.df['retweet_text'] = self.df['retweet_text'].apply(
            lambda x: self.remove_emoji(x))  # remove emoji
        stop = stopwords.words('english')  # remove stopwords
        self.df['retweet_text'] = self.df['retweet_text'].apply(
            lambda x: " ".join(x for x in x.split() if x not in stop))
        self.df['retweet_text'] = self.df['retweet_text'].str.findall(
            r'[a-zA-Z]+')
        self.df['retweet_text'] = self.df['retweet_text'].str.join(' ')
        return self.df

    def parse_source(self) -> pd.DataFrame:
        source = []
        for i in self.df['source'].tolist():
            soup = BeautifulSoup(i, features="lxml")
            loop = soup.a.string
            source.append(loop)
        self.df['source'] = source
        return self.df

    def fill_nullvalues(self):
        self.df['possibly_sensitive'] = self.df['possibly_sensitive'].fillna(
            False)
        self.df['created_at'] = self.df['created_at'].fillna(" ")
        self.df['location'] = self.df['location'].fillna(" ")
        self.df['hashtags'] = self.df['hashtags'].fillna(" ")
        self.df['user_mentions'] = self.df['user_mentions'].fillna(" ")
        self.df['retweet_count'] = self.df['retweet_count'].fillna(0)
        self.df['favorite_count'] = self.df['favorite_count'].fillna(0)
        self.df['followers_count'] = self.df['followers_count'].fillna(0)
        self.df['friends_count'] = self.df['friends_count'].fillna(0)
        self.df['statuses_count'] = self.df['statuses_count'].fillna(0)
        self.df['screen_name'] = self.df['screen_name'].fillna(" ")
        self.df['lang'] = self.df['lang'].fillna(" ")
        self.df['original_text'] = self.df['original_text'].fillna(" ")
        self.df['retweet_text'] = self.df['retweet_text'].fillna(" ")
        self.df['source'] = self.df['source'].fillna(" ")
        return self.df

    def clean_data(self, save=False) -> pd.DataFrame:
        self.df = self.drop_unwanted_column()
        self.df = self.drop_nullValue()
        self.df = self.drop_duplicate()
        self.df = self.convert_to_datetime()
        self.df = self.convert_to_numbers()
        self.df = self.remove_non_english_tweets()
        self.df = self.clean_retweet_text()
        self.df = self.parse_source()
        self.df = self.fill_nullvalues()

        if save:
            self.df.to_csv(
                'data/cleaned_economic_data.csv', index=False)
            print('Cleaned Data Saved !!!')
        return self.df


if __name__ == "__main__":
    df = pd.read_csv("data/extracted_economic_data.csv")
    cleaner = CleanTweets(df)
    cleaner.clean_data(True)
