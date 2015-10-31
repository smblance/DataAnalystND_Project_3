#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017")
db = client.osm

#If collection 'main' present, ask whether user wants to delete it.
print "Collection names: ", db.collection_names()
write_to_main = True
if 'main' in db.collection_names():
	user_input = raw_input('Collection "main" present. Delete it? (y/n): ')
	while user_input not in ('y','n'):
		user_input = raw_input('Input not recognized. Write "y" or "n": ')
	if user_input == 'y':
		write_to_main = True
	elif user_input == 'n':
		write_to_main = False

#If user wants to delete 'main' or 'main' not present, write data to it.
if write_to_main:
	db.drop_collection('main')
	with open('data_cleaned.json') as f:
		data = json.load(f)
	db.main.insert_many(data)
	print db.main.find_one()
	print db.main.count()