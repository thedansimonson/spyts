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

# This is a really awful way to store credentials.
# Originally, they were hard-coded into the script, so this is 
# a little better. 
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
while len(tweets) < config["maximum"]:
    pause = patience.in_minutes(len(queries))
    #try:
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
    """
    except Exception as e:
        print e
        print sys.exc_info()[0]
    """

    print
    print

    patience.wait(pause)
    print "Running..."

#output data
if config["output"] == "pickle":
    pass
elif config["output"] == "json":
    pass
else: 
    print "Probably should have told you this before, but your output"
    print "format is unrecognized. I'm just gonna dump the output as"
    print "json."

    data = json.dumps(tweets)
    open("emergency_dump.json","w").write(data)

    print "See emergency_dump.json for output."

