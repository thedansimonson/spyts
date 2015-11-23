import tweepy
from pprint import pprint

##################
# Initialization #
##################
# Again, probably not the best way to handle this, but it gets the job
# done. More concise than slopping around a credential object.
consumer_key = "NOT SET"
consumer_secret = "NOT SET"
access_token = "NOT SET"
access_token_secret = "NOT SET"

twit = "NOT SET"

def init(config):
    consumer_key = config["consumer_key"]
    consumer_secret = config["consumer_secret"]
    access_token = config["access_token"]
    access_token_secret = config["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twit = tweepy.API(auth) #this is the object to use
    return twit

###########
# Request #
###########
def query(twit, q):
    "Issues a simple query, with some wrapping."
    q = "".join(['"', q,'"'])
    data = twit.search(q)
    return data

#############
# Rearrange #
#############
def DICT(pooi):
    """Take poor object-oriented instance 'pooi' and yield dict.

    It's sort of a weird thing to write a function for, but dict() doesn't work
    on tweepy.models.Status. And quite frankly, I hate objects.
    """

    return pooi.__dict__
    
crap = ["_api"]
dictify = lambda k,x: DICT(x)
def spew(x):
    print x
    return x

fix_technique = {"author":     dictify, 
                 "user":       dictify,
                 #"created_at": lambda k,x: x[k].iso_format()}
                 "created_at": lambda k,x: x.isoformat() 
                                            if "isoformat" in dir(x) else x}
fix_order = [("author",),
             ("user",),
             ("created_at",),
             ("author", "created_at"),
             ("user", "created_at"),
            ]
def clean_data(data):
    data = [DICT(d) for d in data]
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

####################
# Formatted Output #
####################
def dump(d):
    """
    Dumps out the namespace dicts for the argument, along with those for
    d.author and d.user (usually the same--different if RT?)
    """
    pprint(d.__dict__)
    print "\nAuthor"
    pprint(d.author.__dict__)
    print "\nUser"
    pprint(d.user.__dict__)
    print "-"*50


def csv_dump(data, fname):
    """Saves data as a csv to export to fname.
    """
    fob = open(fname, "wb")
    out = csv.DictWriter(fob)
    [out.write(d) for d in data]
    fob.close()

