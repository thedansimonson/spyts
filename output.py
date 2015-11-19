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

crap = ["_api"]
dictify = lambda k,x: the_signal.DICT(x[k])
fix_technique = {"author":     dictify, 
                 "user":       dictify,
                 "created_at": lambda k,x: x[k].iso_format()}
fix_order = [("author",),
             ("user",),
             ("created_at",),
             ("author", "created_at"),
             ("user", "created_at"),
            ]
def clean_data(data):
    data = [the_signal.DICT(d) for d in data]
    [[d.__delitem__(c) for c in crap] for d in data]
    for d in data:
        for F in fix_order:
            #this bit traverses the dictionaries to the point of change
            cursor = d
            for k in F[:-1]:
                cursor = cursor[k]
            # this applies the change to the right spot
            cursor[F[-1]] = fix_technique[F[-1]](F[-1], cursor[F[-1]])

                
    return data

def cycle(string):
    "Fetch data cycle."
    data = clean_data(get(string))
    return data

