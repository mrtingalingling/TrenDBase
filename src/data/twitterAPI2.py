#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : twitterAPI
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


class twitterAPI:
    def __init__(self, *args, **kwargs):
        try:
            OAUTH_TOKEN = CONFIG.get("OAUTH_TOKEN")
            OAUTH_SECRET = CONFIG.get("OAUTH_SECRET")
            CONSUMER_KEY = CONFIG.get("CONSUMER_KEY")
            CONSUMER_SECRET = CONFIG.get("CONSUMER_SECRET")
            TWITTER_HANDLE = CONFIG.get("TWITTER_HANDLE")

            self.auth = OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
            self.t = Twitter(auth=self.auth)
        except Exception as e:
            print(e)

        # self.twitter_userstream = TwitterStream(auth=auth, domain='userstream.twitter.com')
        self.parse_args = self._parse_args()

    def _parse_args(self):
        parser = ArgumentParser()
        parser.add_argument(
            "--verbose",
            required=False,
            action="store_true",
            help="Print input, data, and output",
        )
        # args, trash = parser.parse_known_args(namespace=self.flags)
        args, trash = parser.parse_known_args()

        return args


rate_limit = 500000
# usedRequests =
now = datetime.now(timezone.utc)
remainingDays = calendar.monthrange(now.year, now.month)[1] - int(now.strftime("%d"))
tweetFreq = 10  # How many second per sleep


class tweetListener(twitterAPI):
    def __init__(self, *args, **kwargs):
        # super(tweetListener, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.query_args = dict()
        # if args.track_keywords:
        #     query_args["track"] = args.track_keywords

    # @classmethod
    def streamTweets(self, stream_args: dict = {}):
        stream = TwitterStream(auth=self.auth, **stream_args)
        # if query_args:
        #     tweet_iter = stream.statuses.filter(**query_args)
        # else:
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


def main():
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


# Reference:
# https://github.com/sixohsix/twitter/
# https://github.com/ckoepp/TwitterSearch/blob/master/TwitterSearch/TwitterUserOrder.py
# https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-user-search.py
# http://stackoverflow.com/questions/4698493/can-i-add-custom-methods-attributes-to-built-in-python-types
# http://stackoverflow.com/questions/17140408/if-statement-to-check-whether-a-string-has-a-capital-letter-a-lower-case-letter
