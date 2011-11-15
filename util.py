import collections

LastFMUser = collections.namedtuple('LastFMUser', 'id, country, age, gender, playcount, playlists, friends, crawl_count')

class result:
	playcount = 0.0
	playlists = 0.0
	age = 0.0
	id = 0.0
	friends = 0.0
	crawl_count = 0.0
	samplesize = 0
