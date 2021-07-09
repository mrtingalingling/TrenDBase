from importlib.machinery import SourceFileLoader
from pathlib import Path

userPath = Path.home()
credDir = userPath / "git/.creds"
twitterCred = credDir / "tweet_config.py"
print(twitterCred)
credModules = SourceFileLoader("tweet_config", str(twitterCred)).load_module()
print(credModules)
