#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : Tweet Model
# 	Author  : Ting
#   Version : 1
#   Purpose : It calls twitterAPI and formats the tweets into expected data
#               structure
#
###############################################################################

# Import from Standard Packages
import logging
import traceback
from pprint import pprint
from subprocess import call
import re
from collections import defaultdict
from os.path import join, abspath, dirname, isfile
import csv
from argparse import ArgumentParser
from time import sleep
import importlib as imp
import calendar
from datetime import timezone, datetime, date
import pprint as pp
import requests
import numpy as np
from importlib.machinery import SourceFileLoader
from pathlib import Path

# Import from 3rd Party Packages


# Import local modules
from src.data.twitterAPI2 import twitterAPI, tweetListener
from src.utils.tweetHelper import tweetUtil

rate_limit = 500000
# usedRequests =
now = datetime.now(timezone.utc)
remainingDays = calendar.monthrange(now.year, now.month)[1] - int(now.strftime("%d"))
tweetFreq = 10  # How many second per sleep


class tweetModel(twitterAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @classmethod  # NOTE: Lost all inheritance when you enable the classmethod
    def getTweet(self, username: str = "elonmusk"):
        """Fetch the latest tweet about a target user"""
        tweet = self.t.users.search(q=username, count=1)
        check_time = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")

        return tweet[0], check_time

    def extractTweet(self, username: str = "elonmusk"):
        print(self.t)
        print("-------")
        tweet, check_time = self.getTweet(username)
        print(tweet)
        tweet_content = tweet.get("status").get("text")
        print(f"Latest tweet: {tweet_content}")
        tweet_created_time = tweet.get("status").get("created_at")
        print(f"Tweet Created Time: {tweet_created_time}")
        tweet_hashtag = tweet.get("status").get("entities").get("hashtags")
        print(f"Hashtags: {tweet_hashtag}")
        tweet_symbol = tweet.get("status").get("entities").get("symbols")
        print(f"Symbols: {tweet_symbol}")
        tweet_url = tweet.get("status").get("entities").get("urls")
        print(f"Urls: {tweet_url}")
        tweet_mentions = [
            user_info.get("screen_name")
            for user_info in tweet.get("status").get("entities").get("user_mentions")
        ]
        print(f"User Mentions: {tweet_mentions}")
        tweet_likes = tweet.get("status").get("favorite_count")
        print(f"Tweet Favourites Count: {tweet_likes}")
        tweet_reply_to = tweet.get("status").get("in_reply_to_screen_name")
        print(f"Tweet Reply To: {tweet_reply_to}")

        # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
        account_statuses_count = tweet.get("statuses_count")
        print(f"Statuses Count: {account_statuses_count}")
        account_followers_count = tweet.get("followers_count")
        print(f"Follower Count: {account_followers_count}")
        account_created_time = tweet.get("created_at")
        print(f"Account Created Time: {account_created_time}")
        account_likes = tweet.get("favourites_count")
        print(f"Account Favourites Count: {account_likes}")
        account_follows = tweet.get("friends_count")
        print(f"Account Friends Count: {account_follows}")
        account_listed_count = tweet.get("listed_count")
        print(f"Listed Count: {account_listed_count}")
        account_username = tweet.get("screen_name")
        print(f"User Name: {account_username}")

        return [
            account_username,
            tweet_created_time,
            tweet_content,
            str(tweet_hashtag),
            str(tweet_symbol),
            str(tweet_url),
            str(tweet_mentions),
            tweet_likes,
            tweet_reply_to,
            account_followers_count,
            check_time,
        ]

    def load_tweet_2_google(self, tweet_details):
        pass


def main():
    # Test API
    newTweet = tweetModel()

    # Test Reading Tweet
    # tweet_details = newTweet.extractTweet()
    # while True:
    #     tweet_details = newTweet.extractTweet()
    #     # load_tweet_2_google(tweet_details)  # NOTE: Wll use the import tweet2google module for this

    #     # To prevent abuse of the twitter API and usage limit, calling it only once a minute.
    #     sleep(tweetFreq)

    # Test getting trends
    trends = tweetUtil.getTrend(newTweet.t)
    # print("---")
    print(trends.place(_id=1))
    # print("---")
    # print(trends.available(_woeid=1))

    # Test Uploading Tweet
    # old_tweet = tweet.get('status').get('text')
    # tweetUtil.uploadTweet(tweet, old_tweet)

    # Test Tweet Streams
    # These arguments are optional:
    # stream_args = dict(
    #     timeout=args.timeout,
    #     block=not args.no_block,
    #     heartbeat_timeout=args.heartbeat_timeout,
    # )

    tweetListener().streamTweets()


if __name__ == "__main__":
    # parser = ArgumentParser()
    # parser.add_argument('--filepath', required=True, help="Config file path.")
    # args, trash = parser.parse_known_args()

    # try:
    # 	tweet_config = imp.import_module('CONFIG', args.filepath)
    # except Exception as e:
    # 	print('No CONFIG file found')

    main()
