#########################################################
# SPyTS: The World's Worst Python-based Twitter Scraper #
#########################################################
#
# Dan Simonson, 2015

from pprint import pprint
import patience
import the_signal
import sys
from pickle import dump
import json
import output
import datetime

config_filename = sys.argv[1]
config = json.loads(open(config_filename).read())
con = the_signal.init(config)

#self-explanatory stuff
get = lambda s: the_signal.query(con, s)
get_ids = lambda D: set([d["id"] for d in D])

def cycle(string):
    "Fetch data cycle."
    data = the_signal.clean_data(get(string))
    return data

queries = config["queries"]
tweets = []
ids = set()
while True:
    pause = patience.in_minutes(len(queries))
    try:
        #retrieve
        new_tweets = sum(map(cycle, queries), [])

        #filter
        new_ids = get_ids(new_tweets)
        new_tweets = [n for n, i in zip(new_tweets, new_ids) if i not in ids]

        #retain
        ids |= set(new_ids)
        tweets += new_tweets

        print "Cycle complete."
        print "Total found ids: "+str(len(tweets))
        print "new ids: "+str(len(new_tweets))
        print "Next cycle at "+str(pause)
        
    except Exception as e:
        print "Exception raised during request."
        print e
        print sys.exc_info()[0]
        
        
        
    print
    print
    
    if len(tweets) > config["maximum"]: break
    
    print "Dumping backup... DO NOT BREAK RIGHT NOW."
    dump(tweets, open("BACKUP_TWEETS.pkl", "wb"))
    print "Backup complete. See cycle info above."
    print "You may safely break right now, until the next cycle begins."

    try: patience.wait(pause)
    except KeyboardInterrupt: break #safe escape with break
    print "Running..."

#output data
# always dump the pickle, as a backup
#pprint(tweets)
session_id = str(datetime.datetime.now()).replace(" ",".")
dump(tweets, open("OUTPUT_TWEETS_%s.pkl"%session_id,"wb"))

if config["output"] == "json":
    output.json(tweets, session_id)
elif config["output"] == "csv":
    output.csv(tweets, session_id) 
elif config["output"] == "pickle":
    pass
else: 
    print "Probably should have told you this before, but your output"
    print "format is unrecognized. I'm just gonna dump the output as"
    print "json."
    print
