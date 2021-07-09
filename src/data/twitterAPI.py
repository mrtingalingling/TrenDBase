#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : twitterAPI
# 	Author  : Ting
#   Version : 1
#   Purpose : Finds tweets of certain topics using the official tool
#
###############################################################################

# Import Standard Packages
import requests
import os
import json
import ast

from importlib.machinery import SourceFileLoader
from pathlib import Path

# Import 3rd Party Packages
import pandas as pd
import yaml

userPath = Path.home()
credDir = userPath / "git/.creds"
twitterCred = credDir / "tweet_config.py"
credModules = SourceFileLoader("tweet_config", str(twitterCred)).load_module()


class twitterAPI:
    def __init__(self):
        # data = self.process_yaml()
        # self.bearer_token = credModules.BearerTokens.get("access_token")
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        if not self.bearer_token:
            print("No Twitter Bearer Token Found.")
            return None
        print(self.bearer_token)

    def process_yaml(self):
        with open("config.yaml") as file:
            self.data = yaml.safe_load(file)
            return self.data

    def recent_tweets_search(self, handle="reeldonalddump", max_results=100) -> str:
        mrf = "max_results={}".format(max_results)  # 100
        q = "query=from:{}".format(handle)  # reeldonalddump in str
        url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(mrf, q)
        return url

    # NOTE: From https://developer.twitter.com/en/docs/tutorials/stream-tweets-in-real-time
    # NOTE: From https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py
    def twitter_auth_and_connect(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        response = requests.request("GET", self.bearer_token, headers=headers)
        return response.json()

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FilteredStreamPython"
        return r

    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_token,
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))
        return response.json()

    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

    def set_rules(self, delete):
        # You can adjust the rules if needed
        sample_rules = [
            {"value": "dog has:images", "tag": "dog pictures"},
            {"value": "cat has:images -grumpy", "tag": "cat pictures"},
        ]
        payload = {"add": sample_rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

    def get_stream(self, set):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream",
            auth=self.bearer_oauth,
            stream=True,
        )
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                print(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    twitterCall = twitterAPI()

    rules = twitterCall.get_rules()
    delete = twitterCall.delete_all_rules(rules)
    set = twitterCall.set_rules(delete)
    twitterCall.get_stream(set)


if __name__ == "__main__":
    main()
