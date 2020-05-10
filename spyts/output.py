"""
For saving results from spyts.
"""
import pickle as pkl
import json as jsonlib
from . import the_signal
from pprint import pprint
import csv as csvlib

#TODO: TEMP FIX, but it works
MUST_DELETE = ["retweeted_status",
               "quoted_status",
               "place", #need to unpack properly
               "_json", #redundant info
              ]
def json(tweets, session_id): 
    print("Dumping json...")
    for t in tweets:
        for k in MUST_DELETE:
            if k in t: del t[k]
    data = jsonlib.dumps(tweets, sort_keys=True, 
                         indent=4, separators=(',', ': '))
    open("OUTPUT_%s.json"%session_id,"w").write(data)


def csv(tweets, session_id):
    print("Dumping csv...")
    for t in tweets:
        for k in MUST_DELETE:
            if k in t: del t[k]
    
    for t in tweets:
        for flatten in ["user", "author", "entities"]:
            if flatten in t:
                for k in t[flatten]:
                    t[flatten+"_"+k] = t[flatten][k]
                del t[flatten]
        

    fstream = open("OUTPUT_%s.csv"%session_id,"w")
    headers = sorted(list(tweets[0]))
    writer = csvlib.DictWriter(fstream, fieldnames = headers)

    writer.writeheader()
    for t in tweets:
        t = dict((k,v.encode("utf-8") if str(v) is v else v) for k,v in list(t.items()))
        t = dict((k,v) for k,v in list(t.items()) if k in headers)
        writer.writerow(t)
