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
        num_total_nodes = 0
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
                num_total_nodes = len(db)-3
                print "Crawled count: %s" % num_crawls
                print "Last crawled user: %s" % login
                print "Total entries on DB: %d" % num_total_nodes
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
        for login, info in db.iteritems():
                if isinstance(info, LastFMUser):
                        if info.age == '' or int(info.friends)==0:
                                num_total_nodes -= 1
                                continue
                        unweighted_total_playcount += int(info.playcount)
                        unweighted_total_playlists += int(info.playlists)
                        unweighted_total_age += int(info.age)
                        unweighted_total_id += int(info.id)
                        unweighted_total_friends += int(info.friends)
                        
                        weight = 1/float(info.friends)
                        weighted_total_playcount += int(info.playcount) * weight
                        weighted_total_playlists += int(info.playlists) * weight
                        weighted_total_age += int(info.age) * weight
                        weighted_total_id += int(info.id) * weight
                        weighted_total_friends += int(info.friends) * weight
                        total_weight += weight
                        
        unweighted_average_playcount = float(unweighted_total_playcount) / float(num_total_nodes)
        unweighted_average_playlist = float(unweighted_total_playlists) / float(num_total_nodes)
        unweighted_average_age = float(unweighted_total_age) / float(num_total_nodes)
        unweighted_average_id = float(unweighted_total_id) / float(num_total_nodes)
        unweighted_average_friends = float(unweighted_total_friends) / float(num_total_nodes)
        
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
