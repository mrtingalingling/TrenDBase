#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : Tweet Helper
# 	Author  : Ting
#   Version : 1
#   Purpose : A bunch of helper methods for tweets
#
###############################################################################

# from src.data_models.wordict import define_word


class tweetUtil:
    @staticmethod
    def uploadTweet(self, t, tweet, old_tweet=None):
        if tweet.get("status").get("text") != old_tweet:
            updated_text = self.processText(tweets)
            if updated_text is not None:
                self.sendTweet(t, updated_text)

    @staticmethod
    def getTrend(t):
        """Look for all the trending hashtag"""
        return t.trends

    # TODO: Check how to find retweets
    # def get_retweet(t):
    # 	pass

    @staticmethod
    def sendTweet(self, t, text):
        # This is the part which actually posts the tweet
        if len(text) <= 140:
            # Twitter allows only 140 character tweets
            print("tweetable")

            # Check the lateast tweet to avoid deplicate
            try:
                my_last_tweet = (
                    t.users.search(q="reelDonaldDump", count=1)[0]
                    .get("status")
                    .get("text")
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

    @staticmethod
    def processText(statement):
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

                # NOTE: Need to link define_word to wordict
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
