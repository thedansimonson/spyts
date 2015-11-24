"""
For saving results from spyts.
"""
import pickle as pkl
import json as jsonlib
import the_signal
from pprint import pprint

# TEMP FIX, but it works
MUST_DELETE = ["retweeted_status",
               "place", #need to unpack properly
               "_json", #redundant info
              ]
def json(tweets, session_id, keep = [], remove = []): 
    print "Dumping json..."
    for t in tweets:
        for k in MUST_DELETE:
            if k in t: del t[k]
    data = jsonlib.dumps(tweets, sort_keys=True, 
                         indent=4, separators=(',', ': '))
    open("OUTPUT_%s.json"%session_id,"w").write(data)



