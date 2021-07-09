#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : Tweet Model
# 	Author  : Ting
#   Version : 1
#   Purpose : Finds tweets of certain topics and loads their stats to a
#               GoogleSheet
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
from twitter import Twitter  # , OAuth, TwitterHTTPError, TwitterStream
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.oauth import OAuth
from twitter.util import printNicely

# Import local modules
userPath = Path.home()
credDir = userPath / "git/.creds"
twitterCred = credDir / "tweet_config.py"
credModules = SourceFileLoader("tweet_config", str(twitterCred)).load_module()
CONFIG = credModules.CONFIG


twitterInit = twitterAPI()
t = twitterInit.tweet
rate_limit = 500000
# usedRequests =
now = datetime.now(timezone.utc)
remainingDays = calendar.monthrange(now.year, now.month)[1] - int(now.strftime("%d"))
tweetFreq = 10  # How many second per sleep


def main():
    # tweet_details = extractTweet(t)
    # trends = get_trend(t)
    # print("---")
    # print(trends.place(_id=1))
    # print("---")
    # print(trends.available(_woeid=1))
    # while True:
    #     tweet_details = extractTweet(t)
    # 	# load_tweet(tweet_details)
    #     # To prevent abuse of the twitter API and usage limit, calling it only once a minute.
    #     sleep(tweetFreq)

    # old_tweet = tweet.get('status').get('text')
    # uploadTweet(tweet, old_tweet)

    # These arguments are optional:
    # stream_args = dict(
    #     timeout=args.timeout,
    #     block=not args.no_block,
    #     heartbeat_timeout=args.heartbeat_timeout,
    # )

    streamTweets()


def streamTweets():
    stream_args = dict()
    query_args = dict()
    # if args.track_keywords:
    #     query_args["track"] = args.track_keywords

    stream = TwitterStream(auth=twitterInit.auth, **stream_args)
    if query_args:
        tweet_iter = stream.statuses.filter(**query_args)
    else:
        tweet_iter = stream.statuses.sample()

        # Iterate over the sample stream.
    for tweet in tweet_iter:
        # You must test that your tweet has text. It might be a delete
        # or data message.
        if tweet is None:
            printNicely("-- None --")
        elif tweet is Timeout:
            printNicely("-- Timeout --")
        elif tweet is HeartbeatTimeout:
            printNicely("-- Heartbeat Timeout --")
        elif tweet is Hangup:
            printNicely("-- Hangup --")
        elif tweet.get("text"):
            printNicely(tweet["text"])
        else:
            printNicely("-- Some data: " + str(tweet))


def extractTweet(t):
    tweet, check_time = get_tweet(t)
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


def load_tweet_2_google(tweet_details):
    pass


def uploadTweet(tweet, old_tweet=None):
    if tweet.get("status").get("text") != old_tweet:
        updated_text = process_text(tweets)
        if updated_text is not None:
            send_tweet(t, updated_text)


def get_tweet(t, username="elonmusk"):
    """Fetch the latest tweet about a target user"""
    # users = t.users.search(q='realDonaldTrump', count=1)
    tweet = t.users.search(q=username, count=1)
    check_time = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")

    return tweet[0], check_time


# TODO: Check how to find retweets
# def get_retweet(t):
# 	pass


def get_trend(t):
    """Look for all the trending hashtag"""
    return t.trends


def send_tweet(t, text):
    # This is the part which actually posts the tweet
    if len(text) <= 140:
        # Twitter allows only 140 character tweets
        print("tweetable")

        # Check the lateast tweet to avoid deplicate
        try:
            my_last_tweet = (
                t.users.search(q="reelDonaldDump", count=1)[0].get("status").get("text")
            )
            if my_last_tweet == text:
                print("Content has been tweeted previously, tweet passed.")
                return
        except Exception as e:
            print(e)

        text = text.replace("amp;", "")

        try:
            t.statuses.update(status=text)
        except Exception as e:
            # print e
            print("This is most likely due to deplicate.")

    else:
        print("140 characters crossed")


def process_text(statement):
    text = str(statement["status"]["text"].encode("utf-8"))
    tweet_time = str(statement["status"]["created_at"])
    print("Original Content: " + text + " at " + tweet_time)
    handle = "realDonaldTrump"  # str(statement['screen_name'])

    # Examine the meaning of the tweet
    # Split the tweet into list of words separeted by space
    try:
        updated_text = text.split("....cont")[0]
        text_ls = updated_text.split()

        # For each word and its respective position in the tweet
        for word in text_ls:
            # if 'adjective' in word_lookup.define_word(word).pos:
            # 	text.replace(word, word_lookup.define_word(word).atns[0])
            specific_word = False
            for letter in list(word):
                if letter.isupper():
                    specific_word = True

            if define_word(word) and not specific_word:
                print(word, define_word(word))
                updated_text = updated_text.replace(word, define_word(word))

    except Exception as e:
        print(e)
        return

    print("Proposed Tweet Content: " + updated_text)
    print("Proposed Tweet Length: " + str(len(updated_text)))

    if len(updated_text) + len(handle) + 1 < 140:
        updated_text = "@" + handle + " " + updated_text
        print("Tagged original handler.")
    elif len(updated_text) < 140:
        pass
    else:
        return
        # updated_text = text

    return updated_text


if __name__ == "__main__":
    # parser = ArgumentParser()
    # parser.add_argument('--filepath', required=True, help="Config file path.")
    # args, trash = parser.parse_known_args()

    # try:
    # 	tweet_config = imp.import_module('CONFIG', args.filepath)
    # except Exception as e:
    # 	print('No CONFIG file found')

    main()
