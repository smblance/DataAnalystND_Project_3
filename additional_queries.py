#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017")
db = client.osm

#Count bus stops with/without shelter
bus_stops_total = db.main.find({'highway':'bus_stop'}).count()
bus_stops_with_shelter = db.main.find({'highway':'bus_stop'}, {'shelter' : {'$exists':1}}).count()
print 'Bus stops with shelter: ', bus_stops_with_shelter
print 'Bus stops without: ', bus_stops_total - bus_stops_without_shelter
print '-------------------'

#Most popular leisure types
leisure_types = db.main.aggregate([ \
	{'$match' : {'leisure' : {'$exists' : 1}}}, \
	{'$group' : {'_id' : '$leisure', 'count': {'$sum': 1}}}, \
	{'$sort' : {'count' : -1}}, \
	{'$limit' : 5} \
	])
print 'Most common leisure types:'
for x in leisure_types:
	print x
print '-------------------'

#Most popular sports
sports = db.main.aggregate([ \
	{'$match' : {'sport' : {'$exists' : 1}}}, \
	{'$group' : {'_id' : '$sport', 'count': {'$sum': 1}}}, \
	{'$sort' : {'count' : -1}}, \
	{'$limit' : 5} \
	])
print 'Most common sports.'
for x in sports:
	print x
print '-------------------'

#Most popular shops
shops = db.main.aggregate([ \
	{'$match' : {'shop' : {'$exists' : 1}}}, \
	{'$group' : {'_id' : '$shop', 'count': {'$sum': 1}}}, \
	{'$sort' : {'count' : -1}}, \
	{'$limit' : 5} \
	])
print 'Most common shop types:'
for x in shops:
	print x
print '-------------------'

#Most popular cuisines
cusines = db.main.aggregate([ \
	{'$match' : {'cuisine' : {'$exists' : 1}}}, \
	{'$group' : {'_id' : '$cuisine', 'count': {'$sum': 1}}}, \
	{'$sort' : {'count' : -1}}, \
	{'$limit' : 5} \
	])
print 'Most popular cuisines:'
for x in cusines:
	print x
print '-------------------'

#Most popular cuisines
amenities = db.main.aggregate([ \
	{'$match' : {'amenity' : {'$exists' : 1}}}, \
	{'$group' : {'_id' : '$amenity', 'count': {'$sum': 1}}}, \
	{'$sort' : {'count' : -1}}, \
	{'$limit' : 5} \
	])
print 'Most popular cuisines:'
for x in amenities:
	print x


