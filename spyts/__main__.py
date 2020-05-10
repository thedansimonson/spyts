
#########################################################
# SPyTS: The World's Worst Python-based Twitter Scraper #
#########################################################
#
# Dan Simonson, 2015, 2016, 2020

from pprint import pprint
from . import patience
from . import the_signal
import sys
from pickle import dump
import yaml
from . import output
import datetime


def cycle(string):
    "Fetch data cycle."
    data = the_signal.clean_data(get(string))
    return data



def output_data(tweets):
    "Dump the data appropriately."
    
    # pickle is always output as a backup
    session_id = str(datetime.datetime.now()).replace(" ",".")
    dump(tweets, open("OUTPUT_TWEETS_%s.pkl"%session_id,"wb"))

    if config["output"] == "json":
        output.json(tweets, session_id)
    elif config["output"] == "csv":
        output.csv(tweets, session_id) 
    elif config["output"] == "pickle":
        pass
    else: 
        print("Probably should have told you this before, but your output")
        print("format is unrecognized. Nevertheless, a serialized python pickle")
        print("has been dumped in its stead.")
        print()

def main_loop(config):
    queries = config["queries"]
    tweets = []
    ids = set()
    cycle_counter = 0
    while True:
        pause = patience.in_minutes(len(queries))
        print("Cycle",cycle_counter,"initiated.")
        print("Duration to next cycle:",str(pause))
        try:
            #retrieve
            new_tweets = sum(list(map(cycle, queries)), [])

            #filter
            new_ids = get_ids(new_tweets)
            new_tweets = [n for n, i in zip(new_tweets, new_ids) 
                          if i not in ids]
            
            # reduce memory load (if requested)
            if "arbitrary_clean" in config and config["arbitrary_clean"]:
                new_tweets = list(map(the_signal.clean_brut, new_tweets))

            #retain
            ids |= set(new_ids)
            tweets += new_tweets

            print("Cycle",cycle_counter,"complete.")
            print("Total found ids: "+str(len(tweets)))
            print("new ids: "+str(len(new_tweets)))
            print("Next cycle at "+str(pause))

        except Exception as e:
            print("Exception raised during request.")
            print(e)
            print(sys.exc_info()[0])
            
            
            
        print()
        print()
        
        if config["maximum"] > 0 and len(tweets) > config["maximum"]: break
        
        if "backup" in config and cycle_counter % config["backup"] == 0: 
            print("Dumping backup... DO NOT BREAK RIGHT NOW.")
            dump(tweets, open("BACKUP_TWEETS.pkl", "wb"))
            print("Backup complete. See cycle info above.")
            print()
        
        if ("tweets_per_file" in config and 
            len(tweets) > config["tweets_per_file"]):

            print("Chunk complete. Dumping and emptying tweet cache.")
            print("DO NOT BREAK RIGHT NOW.")
            output_data(tweets)
            tweets = []


        #########################
        # Start the Wait Period #
        #########################

        cycle_counter += 1
        print("You may safely break right now, until the next cycle begins.")
        print("*"*50)
        print()
        try: patience.wait(pause)
        except KeyboardInterrupt: break #safe escape with break
        print("Running...")

    print("Terminal dump initiated. DO NOT BREAK RIGHT NOW.")
    output_data(tweets)
    print("Complete.")



config_filename = sys.argv[1]
config = yaml.load(open(config_filename).read())
con = the_signal.init(config)

#self-explanatory stuff
get = lambda s: the_signal.query(con, s)
get_ids = lambda D: set([d["id"] for d in D])

main_loop(config)
