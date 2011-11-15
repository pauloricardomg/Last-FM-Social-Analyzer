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
from resulttypes import RWResult, RWRWResult
from plot import *

LastFMUser = collections.namedtuple('LastFMUser', 'id, country, age, gender, playcount, playlists, friends, crawl_count')

########################################################################


def main():
        db = 0
        login = "rj"
        num_crawls = 0
        num_total_users = 0
        dbFile = ""
        exist = False

        while(not exist):
                dbFile = raw_input("Crawl DB file (existing file): ")
		#dbFile="randomwalk.db"
                try:
                        open(dbFile)
                        exist = True
                except IOError as e:
                        print 'File %s does not exist.' % (dbFile)
        
        db = None

        try:
                db = shelve.open(dbFile)

                crawl_order = db["crawl-order"]
		login = crawl_order[-1]
                num_crawls = len(crawl_order)

                num_total_users = len(db)-2
                print "Crawled count: %s" % num_crawls
                print "Last crawled user: %s" % login
                print "Total entries on DB: %d" % num_total_users
        except Exception:
                print "DB file not well-formed. Try another one"
                if db != None:
                        db.close()
                        sys.exit(1)

	full_crawl = load_crawl2(db)
	unique = load_unique(db)

	print "Full crawl size: %d" % len(full_crawl)

	random.seed(33)
	
	distributionsDegree2(full_crawl, unique)
	#distributionsDegree(full_crawl)
	#distributionsAge(full_crawl)
	#distributionsPlaycount(full_crawl)
	#distributionsPlaylists(full_crawl)
	#distributionsId(full_crawl)
	
	#ListListRW = []
	#ListListRWRW = []
	#for num_samples in [100, 500, 1000, 2500, 5000, 10000, 25000, 40000]:
	#	ListRW = []
	#	ListRWRW = []
	#	for i in range(20):
	#		random_sample = random.sample(full_crawl, num_samples)
	#		RW, RWRW = analyze(random_sample)
	#		ListRW.append(RW)
	#		ListRWRW.append(RWRW)
	#	ListListRW.append(ListRW)
	#	ListListRWRW.append(ListRWRW)
	#meanAgeVSsampleSize(ListListRW,ListListRWRW)
	db.close()



def analyze(ListLastFMUser):
	RW = RWResult()
	RWRW = RWRWResult()
	
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

def load_crawl2(db):
	crawl_order = db["crawl-order"]
	crawl = []
	for login in crawl_order:
		info = db[login]
		if info.age == '' or int(info.friends) == 0:
			continue
		crawl.append(info)

	return crawl


def load_crawl(db):
	crawl = []
        for login, info in db.iteritems():
                if isinstance(info, LastFMUser):
                        if info.age == '' or int(info.friends)==0:
                                continue
			
			for i in range(int(info.crawl_count)):
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
