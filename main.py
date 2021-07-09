#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : Main
# 	Author  : Ting
#   Version : 1
#   Purpose : Runs the entire system
#
###############################################################################

# Import Standard Packages
from time import sleep
import importlib as imp
import calendar
from datetime import timezone, datetime, date
import pprint as pp

# Import 3rd Party Packages
import pandas as pd

# import gspread

# Import local modules
# from src.utils.twitterAPI import twitterAPI, extractTweet
from src.data.twitterAPI2 import twitterAPI, tweetListener
from src.utils.tweetHelper import tweetUtil
from src.data_models.tweet_model import tweetModel

# from src.utils.gsht_connect import Google_API_Connect

# gsht = Google_API_Connect()
twitterInit = twitterAPI()
t = twitterInit.t
rate_limit = 500000
now = datetime.now(timezone.utc)
remainingDays = calendar.monthrange(now.year, now.month)[1] - int(now.strftime("%d"))
tweetFreq = 10  # How many second per sleep


def main():
    newTweet = tweetModel()
    tweet_details = newTweet.extractTweet()
    # while True:
    #     tweet_details = newTweet.extractTweet()
    #     # load_tweet_2_google(tweet_details)  # NOTE: Wll use the import tweet2google module for this

    #     # To prevent abuse of the twitter API and usage limit, calling it only once a minute.
    #     sleep(tweetFreq)

    # sheet_id = "1Dvi03zxigaUGx2Owpt8JPt5_pxR1I44bEhwEyQtsKJk"
    # gsht.gsht_update(
    #     spreadsheetId=sheet_id,
    #     action="Add",
    #     data_values=[tweet_details],
    #     rangeName="Tweets",
    #     sheet_title_string="Tweets",
    # )

    # Test getting trends
    # trends = tweetUtil.getTrend(newTweet.t)
    # print("---")
    # print(trends.place(_id=1))
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

    # tweetListener().streamTweets()


# 	# load_tweet(tweet_details)
#     # To prevent abuse of the twitter API and usage limit, calling it only once a minute.
#     sleep(tweetFreq)

if __name__ == "__main__":
    main()

