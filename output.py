"""
For saving results from spyts.
"""
import pickle as pkl
import json as jsonlib
import the_signal
from pprint import pprint

def pickle(tweets):
    "The easiest output."
    fo = open("OUTPUT.pkl", "wb")
    dump(tweets, fo)
    fo.close()

def json(tweets, keep = [], remove = []): 
    pprint(tweets)
    data = jsonlib.dumps(tweets)
    open("OUTPUT.json","w").write(data)



