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
from plot import *
from util import LastFMUser, result

def main():
        db_file = ""
        exist = False

        while(not exist):
                db_file = raw_input("Crawl DB file (existing file): ")
                try:
                        open(db_file)
                        exist = True
                except IOError as e:
                        print 'File %s does not exist.' % (db_file)
        
        db = None

        try:
                db = shelve.open(db_file)

                crawl_order = db["crawl-order"]
		login = crawl_order[-1]
                num_crawls = len(crawl_order)

                num_total_users = len(db)-2
                print "Crawl count: %s" % num_crawls
                print "Last crawled user: %s" % login
                print "Unique entries on DB: %d" % num_total_users
        except Exception:
                print "DB file not well-formed. Try another one"
                if db != None:
                        db.close()
                        sys.exit(1)

	crawl_list = load_crawl(db)
	unique_users = load_unique(db)

	analyze(crawl_list)

	plot_visittimes_vs_degree(unique_users)
	plot_degree_distribution(crawl_list)
	plot_age_distribution(crawl_list)
	plot_playlists_distribution(crawl_list)
	plot_playcount_distribution(crawl_list)

	db.close()


def analyze(list_users):
	RW = result()
	RWRW = result()
	
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
        for user in list_users:
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

        num_total_users = len(list_users)
	RW.samplesize = num_total_users
	RWRW.samplesize = num_total_users
	
        RW.playcount = float(unweighted_total_playcount) / float(num_total_users)
        RW.playlists = float(unweighted_total_playlists) / float(num_total_users)
        RW.age = float(unweighted_total_age) / float(num_total_users)
        RW.id = float(unweighted_total_id) / float(num_total_users)
        RW.friends = float(unweighted_total_friends) / float(num_total_users)
        
        RWRW.playcount = float(weighted_total_playcount) / total_weight
        RWRW.playlists = float(weighted_total_playlists) / total_weight
        RWRW.age = float(weighted_total_age) / total_weight
        RWRW.id = float(weighted_total_id) / total_weight
        RWRW.friends = float(weighted_total_friends) / total_weight
        
	print ""
        print "Results for sample size of {}".format(num_total_users)
	print "{0:20s} {1:^15s} {2:^15s}".format("", "RW", "RWRW")
        print "{0:20s} {1:<15f} {2:<15f}".format( "average playcount", RW.playcount, RWRW.playcount)
        print "{0:20s} {1:<15f} {2:<15f}".format( "average playlists", RW.playlists, RWRW.playlists)
        print "{0:20s} {1:<15f} {2:<15f}".format( "average age", RW.age, RWRW.age)
        print "{0:20s} {1:<15f} {2:<15f}".format( "average id", RW.id, RWRW.id)
        print "{0:20s} {1:<15f} {2:<15f}".format( "average friends", RW.friends, RWRW.friends)
	print ""

	return RW, RWRW

# Aux methods

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

def load_crawl(db):
	crawl_order = db["crawl-order"]
	crawl = []
	for login in crawl_order:
		info = db[login]
		if info.age == '' or int(info.friends) == 0:
			continue
		crawl.append(info)

	return crawl

def load_unique(db):
	crawl = []
	for login in db.keys():
        	info = db[login]
		if isinstance(info, LastFMUser):
                	if info.age == '' or int(info.friends) == 0:
				continue
			crawl.append(info)
	return crawl


if __name__ == "__main__":
            main()
