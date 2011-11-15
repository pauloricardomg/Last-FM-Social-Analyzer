import shelve
import collections
import signal
import sys
import urllib2
import xml.etree.ElementTree
import random
import traceback
import time
import datetime
from util import LastFMUser

# Global vars
db = None
crawl_order = []

# Main
def main():
        global db

	# Start from "rj" user
	last_user = "rj"

        db_file = raw_input("Crawl DB file (new or resume): ")
        db = shelve.open(db_file)
        
        try:
		crawl_order = db["crawl-order"]
                # Update "rj" user
		last_user = crawl_order[-1]
		random.setstate(db["random-state"])
                print "Existing crawling data found on %s, resuming crawling.." % db_file
                print "Already crawled %s users so far" % len(crawl_order)
                print "Starting from previously crawled user: %s" % last_user
        except KeyError:
                print "Initializing new crawling DB: %s" % db_file
                random.seed(33)
                pass
	
	# Register signal to flush the DB when CTRL+C is pressed 
        signal.signal(signal.SIGINT, flush_db)
        
        print 'Crawling started. Press Ctrl+C to stop crawling'
        crawl(last_user)

# Crawling loop
def crawl(login):
        global db
	global crawl_order

	# Local vars
	last_login = login
	num_crawls = 0
	chosen_friend = -1
        retry_count = 0

        # Retrieve number of friends for current login
	num_friends = get_num_friends(login)

        while True:
                try:                    
			# It may be a retry
			if chosen_friend == -1:
                                chosen_friend = random.randint(1, num_friends)

			# Chose a random friend from the current login
			friend = get_friend(login, chosen_friend)
			
			# Error in LastFM when a user may have an empty friend
			if friend == None:
				chosen_friend = -1
                                print "[%s] Failed to retrieve friend from %s. Trying to retrieve another friend." % (get_ts(), login)
				continue

			# From this point, the chosen friend becomes the current login
			lastlogin = login
			login = friend.findtext("name")

                        # If it's an existing user, just update the crawl_count
			if db.has_key(login):
                                existing_user = db[login]
                                num_friends = existing_user.friends
                                crawl_count = int(existing_user.crawl_count)
                                
				db[login] = existing_user._replace(crawl_count=str(crawl_count+1))
                                #print "[%s] Already crawled user: %s=%s" % (get_ts(), login, str(db[login]))
                        else:
                                user = get_user_info(friend, login)
				
				# Banned user - Roll back to previous friend, and hopefully will chose another friend of him
				if user.friends == 0:
                                	print "[%s] User %s has 0 friends. Rolling back to user %s" % (get_ts(), login, lastlogin)
					chosen_friend = -1
					login = lastlogin
                                	num_friends = db[login].friends
					continue
				
				db[login] = user
                     
		     	# Append login to crawling order list
			num_crawls = num_crawls+1
			crawl_order.append(login)

			# Update vars
			chosen_friend = -1
                        retry_count = 0
                        
                except Exception as e:
			print "[%s] Error while crawling.." % (get_ts())
                        print e
                        traceback.print_exc(file=sys.stdout)
                        
                        # Typical last fm error, when a banned user is crawled
			if isinstance(e, urllib2.HTTPError) and e.code == 500:
				print "[%s] HTTP error when trying to retrieve info from user %s. Rolling back to user %s" % (get_ts(), login, lastlogin)
				chosen_friend = -1
				login = lastlogin
                                num_friends = db[login].friends
			elif retry_count < 5:
				print "[%s] Retrying. Count: %d" % (get_ts(), retry_count)
				time.sleep(20)
                                retry_count = retry_count + 1
                        else:
                                print "[%s] Already retried 5 times. Saving state and stopping.." % (get_ts())
                                flush_db()
		
		# check-point
		if num_crawls % 100 == 0:
			print "[%s] Crawled %d users. Synchronizing DB.." % (get_ts(), num_crawls)
			save_state()
                        print "[%s] Sleeping 2 seconds. It is safe to stop now. Ctrl+C if you want to quit." % (get_ts())
                        time.sleep(2)
                        print "[%s] Finished sleeping." % (get_ts())

# Aux methods

def get_url(cmd, login, params=""):
        api_key = '974ce2e66dfa37b88f5c004eda97aa55'
        url = "http://ws.audioscrobbler.com/2.0/?method=user.%s&user=%s&api_key=%s%s" % (cmd, login, api_key, params)
        url = url.replace(" ", "%20")
        return url

def get_ts():
        return datetime.datetime.now().isoformat()

def get_num_friends(login):
        url_info = get_url("getfriends", login, "&limit=1")
        data = urllib2.urlopen(url_info).read()
        doc = xml.etree.ElementTree.fromstring(data)
	num_friends = int(doc.find("friends").get("total"))
	return num_friends

def get_friend(login, chosen_friend):
	url_info = get_url("getfriends", login, "&limit=1&page="+str(chosen_friend))
        data = urllib2.urlopen(url_info).read()
        doc = xml.etree.ElementTree.fromstring(data)
        friend = doc.find("friends").find("user")
	return friend

def get_user_info(friend, login):
	user_id = friend.findtext("id")
        country = friend.findtext("country")
        age = friend.findtext("age")
        gender = friend.findtext("gender")
        playcount = friend.findtext("playcount")
        playlists = friend.findtext("playlists")

        num_friends = get_num_friends(login)

        user = LastFMUser(user_id, country, age, gender, playcount, playlists, num_friends, 1)

	return user

def save_state():
	global crawl_order
	
	try:
		total_crawl_order = db["crawl-order"]
		total_crawl_order.extend(crawl_order)
		db["crawl-order"] = total_crawl_order
	except KeyError:
		db["crawl-order"] = crawl_order

	db["random-state"] = random.getstate()
	db.sync()

	crawl_order = []

# Called when CTRL+C is pressed or there is an error
def flush_db(signal="", frame=""):
        print "Crawling finished. Closing DB file.!"

	save_state()
	db.close()
        
	sys.exit(0)

if __name__ == "__main__":
            main()
