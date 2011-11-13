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
num_crawls = 0

def main():
        global db 
        global login
        global num_crawls

        dbFile = raw_input("Crawl DB file (new or resume): ")
        db = shelve.open(dbFile)
        
        try:
                num_crawls = db["num-crawled-logins"]
                login = db["last-crawled-login"]
                random.setstate(db["random-state"])
                print "Existing crawling data found on %s, resuming crawling.." % dbFile
                print "Already crawled %s users so far" % num_crawls
                print "Starting from previously crawled user: %s" % login
        except KeyError:
                print "Initializing new crawling DB: %s" % dbFile
                random.seed(33)
                pass

        signal.signal(signal.SIGINT, flush_db)
        
        print 'Crawling started. Press Ctrl+C to stop crawling'
        crawl()
        signal.pause()

def getURL(cmd, login, params=""):
        api_key = '974ce2e66dfa37b88f5c004eda97aa55'
        url = "http://ws.audioscrobbler.com/2.0/?method=user.%s&user=%s&api_key=%s%s" % (cmd, login, api_key, params)
        url = url.replace(" ", "%20")
        return url

def getTS():
        return datetime.datetime.now().isoformat()

def crawl():
        global login
        global num_crawls
        
        url_info = getURL("getfriends", login, "&limit=1")
        data = urllib2.urlopen(url_info).read()
        doc = xml.etree.ElementTree.fromstring(data)
        num_friends = int(doc.find("friends").get("total"))
        #print "User %s has %d friends" % (login, num_friends)

        chosen_friend = -1
        retry_count = 0

        while True:
                try:                    
                        if chosen_friend == -1:
                                chosen_friend = random.randint(1, num_friends)
                        #print "Actual login: %s, Num friends: %d, Chosen friend: %d" % (login, num_friends, chosen_friend)
                        
                        last_login = login
                        last_numfriends = num_friends
                        url_info = getURL("getfriends", login, "&limit=1&page="+str(chosen_friend))
                        data = urllib2.urlopen(url_info).read()
                        doc = xml.etree.ElementTree.fromstring(data)
                        user_doc = doc.find("friends").find("user")
                        login = user_doc.findtext("name")

                        if db.has_key(login):
                                existing_user = db[login]
                                num_friends = existing_user.friends
                                crawl_count = int(existing_user.crawl_count)
                                db[login] = existing_user._replace(crawl_count=str(crawl_count+1))
                                print "[%s] Already crawled user: %s=%s" % (getTS(), login, str(db[login]))
                        else:
                                user_id = user_doc.findtext("id")
                                country = user_doc.findtext("country")
                                age = user_doc.findtext("age")
                                gender = user_doc.findtext("gender")
                                playcount = user_doc.findtext("playcount")
                                playlists = user_doc.findtext("playlists")

                                url_info = getURL("getfriends", login, "&limit=1")
                                data = urllib2.urlopen(url_info).read()
                                doc = xml.etree.ElementTree.fromstring(data)
                                num_friends = int(doc.find("friends").get("total"))

                                user = LastFMUser(user_id, country, age, gender, playcount, playlists, num_friends, 1)
                                #print login + "=" + str(user)
                                db[login] = user

                        if num_friends == 0:
                                print "[%s] User %s has 0 friends. Rolling back to user %s" % (getTS(), login, last_login)
                                login = last_login
                                num_friends = last_numfriends

                        num_crawls = num_crawls+1
                        chosen_friend = -1
                        retry_count = 0
                        if num_crawls % 100 == 0:
                                print "[%s] Crawled %d users. Synchronizing DB.." % (getTS(), num_crawls)
                                db.sync()
                                print "[%s] Sleeping 2 seconds. It is safe to stop now. Ctrl+C if you want to quit." % (getTS())
                                time.sleep(2)
                                print "[%s] Finished sleeping." % (getTS())


                except Exception as e:
                        traceback.print_exc(file=sys.stdout)
                        print "[%s] Error while crawling.." % (getTS())
                        print e
                        
                        if isinstance(e, urllib2.HTTPError):
                                if e.code == 500:
                                        print "[%s] HTTP error when trying to retrieve info from user %s. Rolling back to user %s" % (getTS(), login, last_login)
                                        login = last_login
                                        num_friends = last_numfriends
                                        chosen_friend = -1
                                        continue

                        if retry_count < 3:
                                retry_count = retry_count + 1
                                print "[%s] Retrying. Count: %d" % (getTS(), retry_count)
                                continue
                        else:
                                print "[%s] Already retried 3 times. Saving state and stopping.." % (getTS())
                                flush_db()



def flush_db(signal="", frame=""):
                global login
                global num_crawls
                print "Crawling finished. Crawled %d users. Closing DB file.!" % num_crawls
                db["last-crawled-login"] = login
                db["num-crawled-logins"] = num_crawls
                db["random-state"] = random.getstate() 
                db.close()
                sys.exit(0)

if __name__ == "__main__":
            main()
