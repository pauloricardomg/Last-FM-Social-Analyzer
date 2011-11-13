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
import math

LastFMUser = collections.namedtuple('LastFMUser', 'id, country, age, gender, playcount, playlists, friends, crawl_count')

def main():
        print variance([1,2,3,4,5])
        db = 0
        login = "rj"
        num_crawls = 0
        num_total_users = 0
        dbFile = ""
        exist = False

        while(not exist):
                dbFile = raw_input("Crawl DB file (existing file): ")
                try:
                        open(dbFile)
                        exist = True
                except IOError as e:
                        print 'File %s does not exist.' % (dbFile)
        
        db = None

        try:
                db = shelve.open(dbFile)
                num_crawls = db["num-crawled-logins"]
                login = db["last-crawled-login"]
                num_total_users = len(db)-3
                print "Crawled count: %s" % num_crawls
                print "Last crawled user: %s" % login
                print "Total entries on DB: %d" % num_total_users
        except Exception:
                print "DB file not well-formed. Try another one"
                if db != None:
                        db.close()
                        sys.exit(1)

        # Do analysis here!
        unweighted_total_playcount = 0
        unweighted_total_playlists = 0
        unweighted_total_age = 0
        unweighted_total_id = 0
        unweighted_total_friends = 0
        
        weighted_total_playcount = 0
        weighted_total_playlists = 0
        weighted_total_age = 0
        weighted_total_id = 0
        weighted_total_friends = 0
        total_weight = 0
        for login, user in db.iteritems():
                if isinstance(user, LastFMUser):
                        if user.age == '' or int(user.friends)==0:
                                num_total_users -= 1
                                continue
                        num_repetition = int(user.crawl_count)
                        unweighted_total_playcount += int(user.playcount) * num_repetition
                        unweighted_total_playlists += int(user.playlists) * num_repetition
                        unweighted_total_age += int(user.age) * num_repetition
                        unweighted_total_id += int(user.id) * num_repetition
                        unweighted_total_friends += int(user.friends) * num_repetition
                        
                        weight = 1/float(user.friends) * num_repetition
                        weighted_total_playcount += int(user.playcount) * weight 
                        weighted_total_playlists += int(user.playlists) * weight
                        weighted_total_age += int(user.age) * weight
                        weighted_total_id += int(user.id) * weight
                        weighted_total_friends += int(user.friends) * weight
                        total_weight += weight
                        
        unweighted_average_playcount = float(unweighted_total_playcount) / float(num_total_users)
        unweighted_average_playlist = float(unweighted_total_playlists) / float(num_total_users)
        unweighted_average_age = float(unweighted_total_age) / float(num_total_users)
        unweighted_average_id = float(unweighted_total_id) / float(num_total_users)
        unweighted_average_friends = float(unweighted_total_friends) / float(num_total_users)
        
        weighted_average_playcount = float(weighted_total_playcount) / total_weight
        weighted_average_playlist = float(weighted_total_playlists) / total_weight
        weighted_average_age = float(weighted_total_age) / total_weight
        weighted_average_id = float(weighted_total_id) / total_weight
        weighted_average_friends = float(weighted_total_friends) / total_weight
        
        
        print "\t\t\t RW \t\t RWRW"
        print "average playcount: \t{}\t{}".format( unweighted_average_playcount, weighted_average_playcount)
        print "average playlists: \t{}\t{}".format( unweighted_average_playlist, weighted_average_playlist)
        print "average age: \t\t{}\t{}".format( unweighted_average_age, weighted_average_age)
        print "average id: \t\t{}\t{}".format( unweighted_average_id, weighted_average_id)
        print "average friends: \t{}\t{}".format( unweighted_average_friends, weighted_average_friends)
                
        db.close()

def analyze(ListLastFMUser)
        unweighted_total_playcount = 0
        unweighted_total_playlists = 0
        unweighted_total_age = 0
        unweighted_total_id = 0
        unweighted_total_friends = 0
        
        weighted_total_playcount = 0
        weighted_total_playlists = 0
        weighted_total_age = 0
        weighted_total_id = 0
        weighted_total_friends = 0
        total_weight = 0
        for user in ListLastFMUser:
                if user.age == '' or int(user.friends)==0:
                        num_total_users -= 1
                        continue
                unweighted_total_playcount += int(user.playcount)
                unweighted_total_playlists += int(user.playlists)
                unweighted_total_age += int(user.age)
                unweighted_total_id += int(user.id)
                unweighted_total_friends += int(user.friends)
                        
                weight = 1/float(user.friends)
                weighted_total_playcount += int(user.playcount) * weight 
                weighted_total_playlists += int(user.playlists) * weight
                weighted_total_age += int(user.age) * weight
                weighted_total_id += int(user.id) * weight
                weighted_total_friends += int(user.friends) * weight
                total_weight += weight

        num_total_users = len(ListLastFMUser)        
        unweighted_average_playcount = float(unweighted_total_playcount) / float(num_total_users)
        unweighted_average_playlist = float(unweighted_total_playlists) / float(num_total_users)
        unweighted_average_age = float(unweighted_total_age) / float(num_total_users)
        unweighted_average_id = float(unweighted_total_id) / float(num_total_users)
        unweighted_average_friends = float(unweighted_total_friends) / float(num_total_users)
        
        weighted_average_playcount = float(weighted_total_playcount) / total_weight
        weighted_average_playlist = float(weighted_total_playlists) / total_weight
        weighted_average_age = float(weighted_total_age) / total_weight
        weighted_average_id = float(weighted_total_id) / total_weight
        weighted_average_friends = float(weighted_total_friends) / total_weight
        
        
        print "\t\t\t RW \t\t RWRW"
        print "average playcount: \t{}\t{}".format( unweighted_average_playcount, weighted_average_playcount)
        print "average playlists: \t{}\t{}".format( unweighted_average_playlist, weighted_average_playlist)
        print "average age: \t\t{}\t{}".format( unweighted_average_age, weighted_average_age)
        print "average id: \t\t{}\t{}".format( unweighted_average_id, weighted_average_id)
        print "average friends: \t{}\t{}".format( unweighted_average_friends, weighted_average_friends)


def add(x,y):
        return x+y

#variance([1,2,3,4,5]) will return 2.0
def variance(valueList):
        sum = reduce(add,valueList)
        length = len(valueList)
        mean = sum / length
        variance = 0.0
        for x in valueList:
                variance += math.pow(x-mean,2)
        return variance / length
                

if __name__ == "__main__":
            main()
