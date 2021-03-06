# SPyTS 
## Simple Python Twitter Scraper

This implements a simple twitter scraper using tweepy. In particular, it tries
to squeeze as much life as possible out of the limited free API requests that
Twitter allows--distributing them through time as evenly as possible. 

It's quick to deploy, small enough to hack if you need different behavior. 
It's intended for basic research purposes, like assembling corpora.

## Setup

You can now use Python 2 or 3. There shouldn't be anything too sensitive
to any specific version now unless tweepy throws a fit.

Install tweepy: http://www.tweepy.org/

Get all associated files for SPyTS:

 * config_example.txt - an example config file (it's JSON)
 * patience.py   - Stuff for... waiting.
 * spyts.py      - This is the one you actually run
 * the_signal.py - A wrapper for tweepy/API stuff

You'll need four keys for using the Twitter API. They change crap all the
time, though, so you'll have to look up exactly what do to get them. They
should be:

 * consumer_key
 * consumer_secret
 * access_token
 * access_token_secret

You get them at by creating a new app: https://apps.twitter.com/
Add these to your config file. 

While you're there, set your queries (must be a list, but if you wanna
just issue one, make a list of one), output (can be "pickle" or "json"),
and maximum number of tweets.

## Running 
Use:
`python spyts.py config.txt`
where config.txt is the json file with your keys and queries.

## Other Config Options

The `consumer_key`, `consumer_secret`, `access_token`, and 
`access_token_secret` are required for scraping tweets. 
Other options are below.

* `queries` (required): list of strings. Queries executed on the API. 
* `maximum` (required): integer. Number of tweets, in excess of, to stop scraping. 
   If less than zero, then it scrapes indefinitely.
* `tweets_per_file` (optional): integer. Number of tweets, in excess of, to dump
   the files currently held in ram, reset the cache, and resume.
   Default behavior: only save at end (excluding back-ups, if enabled)
* `backup` (optional): Integer. Frequency (in cycles) to back-up tweets cached 
   in ram at. 
   Default behavior: do not back-up.


## Notes
For each query you add, SPyTS adds one minute to the wait time. This is 
so you don't go and exhaust your API rate limits.

## Reference

For a scholarly reference, please refer to the paper that spawned this:

Sierra, S. & Simonson, D. (2014) Gender and cool solidarity in Mexican Spanish colloquial phrases. In the Proceedings of New Ways of Analyzing Variation(NWAV) 43, Chicago, IL.

