#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017")
db = client.osm
size = db.main.count()

#Number of documents, nodes, ways
print "Number of documents:", size
print "Number of nodes:", db.main.find({'type':'node'}).count()
print "Number of ways:", db.main.find({'type':'way'}).count()

#Geographical bounding box
bounding_box = db.main.aggregate([\
	{'$group' : {'_id' : 'null', \
	'max_lat' : {'$max' :'$lat'}, 'min_lat' : {'$min' : '$lat'}, \
	'max_lon' : {'$max' : '$lon'}, 'min_lon' : {'$min' : '$lon'}}}, \
	])
print 'Bounding box:'
for x in bounding_box:
	print x

#Entries per user dict
user_data = db.main.aggregate([\
	{'$project': {'user':1, '_id':0}}, \
	{'$group' : {'_id' : '$user', 'count':{'$sum':1}}}, \
	{'$sort' : {'count': -1}}, \
	])

user_data = list(user_data)
contributions_per_user = [x['count'] for x in user_data]
#How many least contributing users make 1% of entries
last_one_pct = 0 
c, pos = 0, -1
while c < size/100.:
	c += user_data[pos]['count']
	last_one_pct += 1
	pos -= 1
#How many users made more than 1% entries each
greater_that_one_pct = [x for x in contributions_per_user if x > size/100.]

print "Number of unique users:",len(user_data)
print "Top contributing user: %s, %s entries."%(user_data[0]['_id'],user_data[0]['count'])
print "Users, who made at least 1%% of entries each: %s."%len(greater_that_one_pct)
print "These users combined made %i%% of the entries."%(float(sum(greater_that_one_pct))/size*100)
print "So, users, who made less than 1%% of entries (less than %i), together made %i%% of the entries."%(size/100.,(1-float(sum(greater_that_one_pct))/size)*100)
print "The %s least contributing users together made 1%% of entries. Each of them made %s entries or less."%(last_one_pct,user_data[pos]['count'])
