from extract_dataframe import TweetDfExtractor
from extract_dataframe import read_json
import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join('fix_bug/')))


_, tweet_list = read_json("data/Economic_Twitter_Data.json")

columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
           'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']


class TestTweetDfExtractor(unittest.TestCase):
    """
                A class for unit-testing function in the fix_clean_tweets_dataframe.py file

                Args:
        -----
                        unittest.TestCase this allows the new class to inherit
                        from the unittest module
        """

    def setUp(self) -> pd.DataFrame:
        self.df = TweetDfExtractor(tweet_list[:2])
        # tweet_df = self.df.get_tweet_df()

    def test_find_statuses_count(self):
        self.assertEqual(self.df.find_statuses_count(), [40, 40])

    def test_find_full_text(self):
        text = ["Die #Deutschen sind ein braves Volk!. Mit #Spritpreisen von 2 Euro abgefunden. Mit #inflation abgefunden. Mit h\u00f6her\u2026 https://t.co/Hu0jivyX2q",
                "Merkel schaffte es in 1 Jahr 1 Million \"Fl\u00fcchtlinge\" durchzuf\u00fcttern, jedoch nicht nach 16 Jahren 1 Million Rentner aus der Armut zu holen."]
        self.assertEqual(self.df.find_full_text(), text)

    def test_find_sentiments(self):
        self.assertEqual(self.df.find_sentiments(self.df.find_full_text()), ([0.16666666666666666, 0.13333333333333333, 0.3166666666666667, 0.08611111111111111, 0.27999999999999997], [
                         0.18888888888888888, 0.45555555555555555, 0.48333333333333334, 0.19722222222222224, 0.6199999999999999]))

    def test_find_created_time(self):
        created_at = ['Fri Apr 22 22:20:18 +0000 2022',
                      'Fri Apr 22 22:19:16 +0000 2022']

        self.assertEqual(self.df.find_created_time(), created_at)

    def test_find_source(self):
        source = ['<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>',
                  '<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>']

        self.assertEqual(self.df.find_source(), source)

    def test_find_screen_name(self):
        name = ['McMc74078966', 'McMc74078966']
        self.assertEqual(self.df.find_screen_name(), name)

    def test_find_followers_count(self):
        f_count = [3, 3]
        self.assertEqual(self.df.find_followers_count(), f_count)

    def test_find_friends_count(self):
        friends_count = [351, 92, 1176, 2704, 30819]
        self.assertEqual(self.df.find_friends_count(), friends_count)

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), [
                         None, None, None, None, None])

    def test_find_favourite_count(self):
        self.assertEqual(self.df.find_favourite_count(),
                         [548, 195, 2, 1580, 72])

    def test_find_retweet_count(self):
        self.assertEqual(self.df.find_retweet_count(), [612, 92, 1, 899, 20])

    def test_find_location(self):
        self.assertEqual(self.df.find_location(), [
                         'Mass', 'Edinburgh, Scotland', None, None, 'United Kingdom'])


if __name__ == '__main__':
    unittest.main()
