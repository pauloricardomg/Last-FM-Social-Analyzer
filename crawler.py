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

LastFMUser = collections.namedtuple('LastFMUser', 'id, country, age, gender, playcount, playlists, friends, crawl_count')
db = 0
login = "rj"
crawl_order = []

def main():
        global db 
        global login

        dbFile = raw_input("Crawl DB file (new or resume): ")
        db = shelve.open(dbFile)
        
        try:
		crawl_order = db["crawl-order"]
                login = crawl_order[-1]
		random.setstate(db["random-state"])
                print "Existing crawling data found on %s, resuming crawling.." % dbFile
                print "Already crawled %s users so far" % len(crawl_order)
		#print "Crawl order: %s" % str(crawl_order) 
                print "Starting from previously crawled user: %s" % login
        except KeyError:
                print "Initializing new crawling DB: %s" % dbFile
                random.seed(33)
                pass

        signal.signal(signal.SIGINT, flush_db)
        
        print 'Crawling started. Press Ctrl+C to stop crawling'
        crawl()

def get_url(cmd, login, params=""):
        api_key = '974ce2e66dfa37b88f5c004eda97aa55'
        url = "http://ws.audioscrobbler.com/2.0/?method=user.%s&user=%s&api_key=%s%s" % (cmd, login, api_key, params)
        url = url.replace(" ", "%20")
        return url

def getTS():
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
 

def crawl():
        global login
	global crawl_order
	num_crawls = 0
        
        num_friends = get_num_friends(login)

        chosen_friend = -1
        retry_count = 0

        while True:
                try:                    
			if chosen_friend == -1:
                                chosen_friend = random.randint(1, num_friends)
                        
			friend = get_friend(login, chosen_friend)
			login = friend.findtext("name")

                        if db.has_key(login):
                                existing_user = db[login]
                                num_friends = existing_user.friends
                                crawl_count = int(existing_user.crawl_count)
                                db[login] = existing_user._replace(crawl_count=str(crawl_count+1))
                                print "[%s] Already crawled user: %s=%s" % (getTS(), login, str(db[login]))
                        else:
                                user_id = friend.findtext("id")
                                country = friend.findtext("country")
                                age = friend.findtext("age")
                                gender = friend.findtext("gender")
                                playcount = friend.findtext("playcount")
                                playlists = friend.findtext("playlists")

                                num_friends = get_num_friends(login)

                                user = LastFMUser(user_id, country, age, gender, playcount, playlists, num_friends, 1)
				db[login] = user
                      
			chosen_friend = -1
                        retry_count = 0
                        
			if num_friends == 0:
                                print "[%s] User %s has 0 friends. Rolling back to user %s" % (getTS(), login, crawl_order[-1])
                                login = crawl_order[-1]
                                num_friends = db[login].friends
				continue

                        num_crawls = num_crawls+1
			crawl_order.append(login)
			if num_crawls % 100 == 0:
                               	print "[%s] Crawled %d users. Synchronizing DB.." % (getTS(), num_crawls)
				try:
					total_crawl_order = db["crawl-order"]
					total_crawl_order.extend(crawl_order)
					db["crawl-order"] = total_crawl_order
				except KeyError:
					db["crawl-order"] = crawl_order
				crawl_order = []
				db["random-state"] = random.getstate() 
				db.sync()
                               	print "[%s] Sleeping 5 seconds. It is safe to stop now. Ctrl+C if you want to quit." % (getTS())
                               	time.sleep(5)
                               	print "[%s] Finished sleeping." % (getTS())

                except Exception as e:
			print "[%s] Error while crawling.." % (getTS())
                        print e
                        traceback.print_exc(file=sys.stdout)
                        
                        if isinstance(e, urllib2.HTTPError) and e.code == 500:
				print "[%s] HTTP error when trying to retrieve info from user %s. Rolling back to user %s" % (getTS(), login, crawl_order[-1])
                                login = crawl_order[-1]
                                num_friends = db[login].friends
				chosen_friend = -1
                                continue

                        if retry_count < 5:
                                print "[%s] Retrying. Count: %d" % (getTS(), retry_count)
				time.sleep(5)
                                retry_count = retry_count + 1
                                continue
                        else:
                                print "[%s] Already retried 5 times. Saving state and stopping.." % (getTS())
                                flush_db()



def flush_db(signal="", frame=""):
                global login
		global crawl_order
                print "Crawling finished. Closing DB file.!"
	
		try:
			total_crawl_order = db["crawl-order"]
			total_crawl_order.extend(crawl_order)
			db["crawl-order"] = total_crawl_order
		except KeyError:
			db["crawl-order"] = crawl_order
	
		db["random-state"] = random.getstate() 
		db.close()
                sys.exit(0)

if __name__ == "__main__":
            main()
